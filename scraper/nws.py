import logging
from playwright.sync_api import sync_playwright


class NWSScraper:
    provider = "nws"
    URL = "https://forecast.weather.gov/MapClick.php?lat=38.870681&lon=-106.980937"

    def fetch(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto(self.URL, wait_until="domcontentloaded", timeout=15000)
            page.wait_for_timeout(1000)

            temp = page.locator(".myforecast-current-lrg").first.inner_text()
            desc = page.locator(".myforecast-current").first.inner_text()
            feels = "N/A"

            browser.close()

            return {
                "provider": self.provider,
                "temperature": temp,
                "description": desc,
                "feels_like": feels,
                "url": self.URL,
            }
