import logging
from playwright.sync_api import sync_playwright


class WeatherBugScraper:
    provider = "weatherbug"
    URL = "https://www.weatherbug.com/weather-forecast/now/crested-butte-co-81224"

    def fetch(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto(self.URL, wait_until="domcontentloaded", timeout=15000)
            page.wait_for_timeout(1000)

            temp = page.locator(
                '[class*="obsTemperature__ObsTemperature"]'
            ).first.inner_text()
            desc = page.locator(
                '[class*="currentConditionIconDescription__CurrentConditionIconDescription"]'
            ).first.inner_text()
            feels = page.locator(
                '[class*="obsFeelsLike__ObsFeelsLike"]'
            ).first.inner_text()

            browser.close()

            return {
                "provider": self.provider,
                "temperature": temp,
                "description": desc,
                "feels_like": feels,
                "url": self.URL,
            }
