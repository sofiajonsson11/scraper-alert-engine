import os
import time
import logging
import schedule
from dotenv import load_dotenv

from scraper.weather_bug_scraper import fetch_weather_bug
from storage.db import init_db, save_weather, get_last_weather, has_meaningful_change
from alerts.email_alerts import send_email

# Load environment variables
load_dotenv()
URL = os.getenv("TARGET_URL")
EMAIL_INTERVAL = 10  # minutes

# Ensure logs folder exists
os.makedirs("logs", exist_ok=True)

# Configure logging
logging.basicConfig(
    filename="logs/scraper.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def run_scraper():
    logging.info("Running scraper...")
    try:
        data = fetch_weather_bug(URL)
    except Exception as e:
        logging.error(f"Error fetching data: {e}")
        return

    last_record = get_last_weather()

    if has_meaningful_change(new_data=data, old_data=last_record):
        logging.info("Meaningful change detected! Sending email alert...")

        subject = f"Weather Update: {data['description']} at {data['temperature']}"
        body = (
            f"{data['description']} at {data['temperature']} "
            f"(Feels like {data['feels_like']})\n{data['url']}"
        )

        if send_email(subject, body):
            logging.info("Email sent successfully.")
        else:
            logging.error("Failed to send email.")

        # Save the new data after alert
        save_weather(data)
        logging.info(f"New weather data saved: {data}")
    else:
        logging.info("No meaningful change detected. Skipping save and email.")

    logging.info("Done scraping.\n")


if __name__ == "__main__":
    init_db()

    # Run immediately first
    run_scraper()

    # Schedule scraping every 10 minutes
    schedule.every(EMAIL_INTERVAL).minutes.do(run_scraper)
    logging.info("Scheduler started. Press Ctrl+C to stop.")

    while True:
        schedule.run_pending()
        time.sleep(1)
