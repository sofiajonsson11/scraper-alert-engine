from email.message import EmailMessage
import smtplib
import os

EMAIL = os.getenv("EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
ALERT_EMAIL = os.getenv("ALERT_EMAIL")


def send_email(subject, body):
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL
    msg["To"] = ALERT_EMAIL

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL, EMAIL_PASSWORD)
        smtp.send_message(msg)
