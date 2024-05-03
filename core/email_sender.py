import smtplib
import os

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(to_email, subject, body):
    sender_email = os.environ.get('EMAIL')
    sender_password = os.environ.get('EMAIL_PASSWORD')
    smtp_server = os.environ.get('SMTP_PORT')
    smtp_port = os.environ.get('SMTP_PORT')

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = to_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, message.as_string())
        server.quit()
    except Exception as e:
        print('e: ', e)