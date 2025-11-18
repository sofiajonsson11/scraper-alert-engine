import schedule
import time
import logging
import os
from dotenv import load_dotenv

from scraper.weather_bug_scraper import fetch_weather_bug
from scraper.rules import should_alert
from storage.repository import item_exists, save_item, get_latest_items
from storage.db import init_db
from alerts.email_alerts import send_email

# Load environment variables
load_dotenv()

TARGET_URL = os.getenv("TARGET_URL")

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
        data = fetch_weather_bug(TARGET_URL)
    except Exception as e:
        logging.error(f"Error fetching data: {e}")
        return

    if not item_exists(data["url"], data["description"], data["temperature"]):
        logging.info("Saving new data to DB...")
        save_item(
            data["temperature"], data["description"], data["feels_like"], data["url"]
        )

        if should_alert(data):
            logging.info("Alert triggered! Sending email...")
            send_email(
                "Weather Alert for Irwin, CO!",
                f"{data['description']} at {data['temperature']} (Feels like {data['feels_like']})\n{data['url']}",
            )
    else:
        logging.info("Data already exists, skipping save.")

    logging.info(f"Scraped data: {data}")

    # Show last 5 entries in DB
    latest = get_latest_items()
    logging.info("Latest entries in DB:")
    for row in latest:
        logging.info(row)

    logging.info("Done scraping.\n")


if __name__ == "__main__":
    init_db()

    # Run immediately first
    run_scraper()

    # Schedule to run every 10 minutes
    schedule.every(10).minutes.do(run_scraper)

    logging.info("Scheduler started. Press Ctrl+C to stop.")
    while True:
        schedule.run_pending()
        time.sleep(1)
