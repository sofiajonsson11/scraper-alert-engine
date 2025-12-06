import logging
import time
from playwright.sync_api import sync_playwright


class AccuWeatherScraper:
    provider = "AccuWeather"

    def __init__(self, debug=False):
        self.debug = debug  # if True: keeps browser open

    def fetch(self):
        url = "https://www.accuweather.com/en/us/crested-butte/81224/current-weather/332226"
        logging.info(f"{self.provider} fetch started: {url}")

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=not self.debug)
                page = browser.new_page()

                # Retry page load (AccuWeather errors often)
                MAX_RETRIES = 5
                for attempt in range(1, MAX_RETRIES + 1):
                    try:
                        logging.info(f"{self.provider} attempt {attempt} loading page")
                        page.goto(url, timeout=30000)
                        page.wait_for_selector(
                            "div.current-weather-card", timeout=20000
                        )
                        break
                    except Exception as e:
                        logging.error(f"{self.provider} attempt {attempt} failed: {e}")
                        if attempt == MAX_RETRIES:
                            raise
                        time.sleep(1)

                # Extract temperature
                temp_element = page.query_selector(
                    "div[class*='current-weather-info'] div.temp"
                )
                temp = temp_element.inner_text() if temp_element else "N/A"

                # Extract feels-like
                feels_element = page.query_selector(
                    "div[class*='current-weather-extra no-realfeel-phrase']"
                )
                feels_like = feels_element.inner_text() if feels_element else "N/A"

                # Extract description
                desc_element = page.query_selector(
                    "div[class*='current-weather'] div.phrase"
                )
                description = desc_element.inner_text() if desc_element else "N/A"

                data = {
                    "provider": "accuweather",
                    "temperature": temp,
                    "feels_like": feels_like,
                    "description": description,
                    "url": url,
                }

                logging.info(f"{self.provider} scraped: {data}")

                if self.debug:
                    logging.info(f"{self.provider} debug mode: browser open for 30s")
                    time.sleep(30)

                browser.close()
                return data

        except Exception as e:
            logging.error(f"{self.provider} failed: {e}", exc_info=True)
            return None
