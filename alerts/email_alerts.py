from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
ALERT_EMAIL = os.getenv("ALERT_EMAIL")


def send_email(subject: str, message: str, html: str | None = None) -> bool:
    """
    Send an email alert using Gmail SMTP.

    Args:
        subject: Email subject line.
        message: Plain-text fallback message.
        html: Optional HTML version of the email.

    Returns:
        True if sent successfully, False otherwise.
    """

    try:
        # Build email container
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = EMAIL
        msg["To"] = ALERT_EMAIL

        # Attach plain text version
        msg.attach(MIMEText(message, "plain"))

        # Attach HTML version if provided
        if html:
            msg.attach(MIMEText(html, "html"))

        # Send email via Gmail SMTP
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL, EMAIL_PASSWORD)
            smtp.send_message(msg)

        logging.info(f"Email sent: {subject}")
        return True

    except Exception as e:
        logging.error(f"Failed to send email: {e}")
        return False
