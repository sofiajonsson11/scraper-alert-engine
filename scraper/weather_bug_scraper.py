import logging
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import time


def fetch_weather_bug(url: str, retries: int = 3, wait_time: float = 2.0) -> dict:
    """
    Scrape WeatherBug page for current weather data.

    Args:
        url: URL of the WeatherBug page.
        retries: Number of retry attempts if scraping fails.
        wait_time: Wait time between retries (seconds).

    Returns:
        dict with temperature, description, feels_like, and url
    """
    for attempt in range(1, retries + 1):
        try:
            with sync_playwright() as p:
                # Headless browser
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()

                # Go to target URL
                page.goto(url, timeout=60000, wait_until="domcontentloaded")
                time.sleep(wait_time)  # allow JS to populate

                # Handle popups dynamically (close if exists)
                try:
                    popup = page.query_selector(
                        "div[class*='popup'], div[class*='modal']"
                    )
                    if popup:
                        close_button = popup.query_selector(
                            "button, .close, .close-button"
                        )
                        if close_button:
                            close_button.click()
                            logging.info("Popup closed successfully")
                except Exception:
                    pass  # ignore if no popup

                # Scrape dynamic elements
                temp_elem = page.query_selector("div[class^='obsTemp']")
                desc_elem = page.query_selector(
                    "div[class^='currentConditionIconDescription']"
                )
                feels_like_elem = page.query_selector("div[class^='obsFeelsLike']")

                temperature = temp_elem.inner_text() if temp_elem else "N/A"
                description = desc_elem.inner_text() if desc_elem else "N/A"
                feels_like = feels_like_elem.inner_text() if feels_like_elem else "N/A"

                browser.close()

                logging.info(
                    f"Weather fetched: {temperature}, {description}, {feels_like}"
                )
                return {
                    "temperature": temperature,
                    "description": description,
                    "feels_like": feels_like,
                    "url": url,
                }

        except PlaywrightTimeoutError:
            logging.warning(f"Attempt {attempt} timed out, retrying...")
        except Exception as e:
            logging.error(f"Attempt {attempt} failed: {e}")

        time.sleep(wait_time)

    # If all retries fail, return N/A
    logging.error("All attempts to fetch WeatherBug data failed.")
    return {"temperature": "N/A", "description": "N/A", "feels_like": "N/A", "url": url}


if __name__ == "__main__":
    test_url = "https://www.weatherbug.com/weather-forecast/now/crested-butte-co-81224"
    data = fetch_weather_bug(test_url)
    print(data)
