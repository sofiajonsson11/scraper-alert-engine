import yagmail
from dotenv import load_dotenv
import os

load_dotenv()

SENDER = os.getenv("EMAIL")
PASSWORD = os.getenv("EMAIL_PASSWORD")
RECIPIENT = os.getenv("ALERT_EMAIL")


def send_email(subject, body):
    yag = yagmail.SMTP(SENDER, PASSWORD)
    yag.send(to=RECIPIENT, subject=subject, contents=body)
