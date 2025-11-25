from scraper.weather_bug_scraper import fetch_weather_bug
from scraper.rules import should_alert
from alerts.email_alerts import send_email
from storage.db import (
    get_latest_weather,
    init_db,
    save_weather,
    get_last_weather,
    has_meaningful_change,
)
import schedule, time, logging, os
from dotenv import load_dotenv

load_dotenv()
TARGET_URL = os.getenv("TARGET_URL")
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/scraper.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def run_scraper():
    logging.info("Running scraper...")

    try:
        new_data = fetch_weather_bug(TARGET_URL)
    except Exception as e:
        logging.error(f"Error fetching data: {e}")
        return

    # Get the last saved record from the database
    last_record = get_latest_weather()  # returns dict or None

    if has_meaningful_change(new_data, last_record):
        logging.info(
            f"Meaningful change detected:\nOld: {last_record}\nNew: {new_data}"
        )

        # Send email alert first
        email_sent = send_email(
            subject=f"Weather Alert for Crested Butte, CO!",
            message=f"{new_data['description']} at {new_data['temperature']} "
            f"(Feels like {new_data['feels_like']})\n{new_data['url']}",
        )

        if email_sent:
            logging.info("Email alert sent successfully.")
        else:
            logging.warning("Email alert failed.")

        # Save new data to the database
        save_weather(new_data)
        logging.info(f"New data saved: {new_data}")

    else:
        logging.info("No meaningful change detected, skipping email and save.")

    logging.info("Done scraping.\n")


if __name__ == "__main__":
    init_db()
    run_scraper()
    schedule.every(10).minutes.do(run_scraper)
    logging.info("Scheduler started. Press Ctrl+C to stop.")
    while True:
        schedule.run_pending()
        time.sleep(1)
