from playwright.sync_api import sync_playwright


def fetch_weather_bug(url: str, retries: int = 3, wait_time: float = 2.0) -> dict:
    """Scrape WeatherBug page for Irwin, CO weather data."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # True for scheduled runs
        page = browser.new_page()

        page.goto(url, timeout=60000, wait_until="domcontentloaded")
        page.wait_for_timeout(2000)  # wait for JS to populate elements

        # Try matching dynamic WeatherBug classes
        try:
            temp_elem = page.query_selector("div[class^='obsTemp']")
            desc_elem = page.query_selector(
                "div[class^='currentConditionIconDescription']"
            )
            feels_like_elem = page.query_selector("div[class^='obsFeelsLike']")

            temperature = temp_elem.inner_text() if temp_elem else "N/A"
            description = desc_elem.inner_text() if desc_elem else "N/A"
            feels_like = feels_like_elem.inner_text() if feels_like_elem else "N/A"

        except Exception as e:
            print(f"Error scraping WeatherBug: {e}")
            temperature = description = feels_like = "N/A"

        browser.close()

        return {
            "temperature": temperature,
            "description": description,
            "feels_like": feels_like,
            "url": url,
        }


if __name__ == "__main__":
    url = "https://www.weatherbug.com/weather-forecast/now/irwin-co-81230"
    print(fetch_weather_bug(url))
