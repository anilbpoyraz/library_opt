from core.celery import celery_app

from celery.utils.log import get_task_logger
from celery.schedules import crontab

from api import deps
from datetime import datetime, timedelta

from fastapi import Depends
from sqlalchemy.orm import Session

from sqlalchemy.orm import sessionmaker

from db.database import SessionLocal


from typing import Any
from core.email_sender import send_email

import models
import controller
from api.deps import get_db

logger = get_task_logger(__name__)

db = SessionLocal()
TODAY = datetime.now()

def get_overdue_books():
    """ get datas from Transaction table """

    overdue_transactions = db.query(models.Transaction).filter(
        models.Transaction.return_date > TODAY,
        models.Transaction.is_active == True).all()

    return overdue_transactions


def get_previous_week_checkedout_books():
    """ get datas from CheckOutBook table """
    week_before = TODAY - timedelta(days=7)
    return_in_time_books = db.query(models.CheckedOutBook).filter(
        models.CheckedOutBook.is_return_on_time == True,
        models.CheckedOutBook.transactions.checkout_date.between(TODAY, week_before),
    )
    return_not_in_time_books = db.query(models.CheckedOutBook).filter(
        models.CheckedOutBook.is_return_on_time == False,
        models.CheckedOutBook.transactions.checkout_date.between(TODAY, week_before),
    )

    data = {
        'return_in_time_books': return_in_time_books,
        'return_not_in_time_books': return_not_in_time_books,
    }

    return data

@celery_app.task
def send_overdue_reminder_email():
    """ Task that send remainder email to whom couldn't bring back the book """
    overdue_books = get_overdue_books()
    if overdue_books and len(overdue_books) > 0:
        for transaction in overdue_books:
            to_email = transaction.patrons.email
            book_title = transaction.books.title
            mail_subject = 'Library Reminder'
            mail_body = f"The purpose of this email is to remind you that the return date of {book_title}, you borrowed from the library."
            print('transaction: ', transaction)
            # TODO arrange smtp eniroment params
            # send_email(to_email, mail_subject, mail_body)
    
@celery_app.task
def  generate_checkout_statistic_report():
    """ Task that generate a report on checkout books statistics """
    checkout_books = get_previous_week_checkedout_books()
    print('checkout_books: ', checkout_books)
    # TODO report model
    # generate_report(checkout_books)


celery_app.conf.beat_schedule = {
    "library-reminder-daily-email-task": {
        "task": "tasks.send_overdue_reminder_email",
        "schedule": crontab(hour=10, minute=30)
    },
   
    "generate-checkout-statistic-report-task": {
        "task": "tasks.generate_checkout_statistic_report",
        "schedule": crontab(hour=10, minute=30, day_of_week=1)
    }
   
}
