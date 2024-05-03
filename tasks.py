from core.celery import celery_app

from celery.utils.log import get_task_logger
from celery.schedules import crontab

from api import deps
from datetime import datetime, timedelta

from fastapi import Depends
from sqlalchemy.orm import Session

from typing import Any
from core.email_sender import send_email

import models

logger = get_task_logger(__name__)

@staticmethod
def get_overdue_book(
    db: Session = Depends(deps.get_db)
) -> Any:
    today = datetime.now()
    overdue_transactions = db.query(models.Transaction).filter(
            models.Transaction.return_date < today).all()

    return overdue_transactions

@celery_app.task
async def send_overdue_reminder_email():
    print('hello celery!!')
    overdue_transactions = get_overdue_book
    for transaction in overdue_transactions:
        patron_email = transaction.patrons.email
        mail_subject = 'Library Reminder'
        mail_body = f"The purpose of this email is to remind you that the return date of a {book} you borrowed from the library."
        book = transaction.books.title
        send_email(patron_email, mail_subject, mail_body)

@celery_app.task
async def  generate_checkout_statistic_report():
    pass

celery_app.conf.beat_schedule = {
    "library-reminder-task": {
        "task": "tasks.send_overdue_reminder_email",
        "schedule": crontab(hour=10, minute=30)
    },
    "generate-checkout-statistic-report-task": {
        "task": "tasks.generate_checkout_statistic_report",
        "schedule": crontab(hour=10, minute=30, day_of_week=1)
    }
}
