from scraper.fetch import fetch_html
from scraper.parse import parse_example_page
from scraper.rules import should_alert
from scraper.weather_com_scraper import fetch_weather_com
from storage.repository import save_item
from storage.db import init_db
from alerts.email_alerts import send_email
import schedule
import time
import os
from dotenv import load_dotenv


load_dotenv()

URL = "https://www.weatherbug.com/weather-forecast/now/irwin-co-81230"  # Irwin, CO canonicalCityId


def run_scraper():
    print("Starting run_scraper()...")
    try:
        data = fetch_weather_com(URL)
        print(f"Fetched data: {data}")  # DEBUG
        if should_alert(data):
            print("Alert condition met!")  # DEBUG
            save_item(data["description"], data["temperature"], data["url"])
            send_email(
                "Weather Alert!",
                f"{data['description']} at {data['temperature']} in Irwin, CO",
            )
        else:
            print("No alert triggered.")  # DEBUG
    except Exception as e:
        print(f"Error occurred: {e}")
    print("Done run_scraper()")


if __name__ == "__main__":
    test_url = "https://www.weatherbug.com/weather-forecast/now/irwin-co-81230"
    print(fetch_weather_com(test_url))

    # init_db()

    # print("Running scraper immediately...")
    # run_scraper()  # Run once at startup

    # schedule.every(10).minutes.do(run_scraper)
    # print("Scheduler started.")
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
