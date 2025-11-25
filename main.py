from scraper.weather_bug_scraper import fetch_weather_bug
from scraper.rules import should_alert
from alerts.email_alerts import send_email
from storage.db import init_db, save_weather, get_last_weather, has_meaningful_change
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
    data = fetch_weather_bug(TARGET_URL)

    last_record = get_last_weather(TARGET_URL)
    if has_meaningful_change(data, last_record):
        save_weather(
            data["temperature"], data["description"], data["feels_like"], data["url"]
        )
        logging.info(f"New data saved: {data}")

        if should_alert(data):
            send_email(
                "Weather Alert",
                f"{data['description']} at {data['temperature']} (Feels like {data['feels_like']})\n{data['url']}",
            )
    else:
        logging.info("No meaningful change, skipping save and alert.")


if __name__ == "__main__":
    init_db()
    run_scraper()
    schedule.every(10).minutes.do(run_scraper)
    logging.info("Scheduler started. Press Ctrl+C to stop.")
    while True:
        schedule.run_pending()
        time.sleep(1)
