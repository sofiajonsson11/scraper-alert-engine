from scraper.weather_bug_scraper import fetch_weather_bug
from storage.repository import item_exists, save_item, get_latest_items
from storage.db import init_db
from alerts.email_alerts import send_email
import schedule
import time
import os

URL = "https://www.weatherbug.com/weather-forecast/now/irwin-co-81230"  # Irwin, CO weather page


def should_alert(data):
    """Example rule: send alert if temperature < 32°F or 'Snow' in description."""
    temp_value = "".join(filter(str.isdigit, data["temperature"]))
    if temp_value and int(temp_value) < 32:
        return True
    if "snow" in data["description"].lower():
        return True
    return False


def run_scraper():
    print("Running scraper...")
    data = fetch_weather_bug(URL)

    if not item_exists(data["url"], data["description"], data["temperature"]):
        print("Saving new data to DB...")
        save_item(
            data["temperature"], data["description"], data["feels_like"], data["url"]
        )

        if should_alert(data):
            send_email(
                "Weather Alert for Irwin, CO!",
                f"{data['description']} at {data['temperature']} (Feels like {data['feels_like']})\n{data['url']}",
            )
    else:
        print("Data already exists, skipping save.")

    print(f"Scraped data: {data}")

    # Show last 5 entries in DB
    latest = get_latest_items()
    print("Latest entries in DB:")
    for row in latest:
        print(row)

    print("Done scraping.\n")


if __name__ == "__main__":
    init_db()

    # Run immediately first
    run_scraper()  # Run once at startup

    # Schedule to run every 10 minutes
    schedule.every(10).minutes.do(run_scraper)

    print("Scheduler started. Press Ctrl+C to stop.")
    while True:
        schedule.run_pending()
        time.sleep(1)
