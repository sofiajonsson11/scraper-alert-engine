import logging
import os
from scraper.accuweather import AccuWeatherScraper
from scraper.weatherbug import WeatherBugScraper
from scraper.nws import NWSScraper
from storage.db import init_db, save_weather

# Ensure the logs directory exists
os.makedirs("logs", exist_ok=True)

# Configure logging
log_file = "logs/scraper.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file),  # write logs to file
        logging.StreamHandler(),  # also output to terminal
    ],
)


def main():
    logging.info("Starting weather scraping...")
    init_db()

    scrapers = [
        AccuWeatherScraper(debug=True),
        WeatherBugScraper(),
        NWSScraper(),
    ]

    for scraper in scrapers:
        logging.info(f"Fetching data from {scraper.provider}...")
        try:
            data = scraper.fetch()
            if data is None:
                logging.warning(
                    f"No data returned from {scraper.provider}. Skipping save."
                )
                continue

            logging.info(f"{scraper.provider} data: {data}")
            save_weather(data)

        except Exception as e:
            logging.error(f"{scraper.provider} failed: {e}", exc_info=True)
            continue

    logging.info("Weather scraping completed.")


if __name__ == "__main__":
    main()
