from abc import ABC, abstractmethod
import datetime


class BaseScraper(ABC):
    provider: str = "base"

    @abstractmethod
    async def fetch(self, page):
        """Navigate and Fetch HTML content with Playwright"""
        pass

    @abstractmethod
    def parse(self, html: str):
        """Extract raw fields from HTML content"""
        pass

    @abstractmethod
    def normalize(self, parsed):
        """Convert parsed fields to a standard dictionary format"""
        pass

    async def run(self, page):
        """Full scraping process: fetch, parse, normalize"""
        html = await self.fetch(page)
        parsed = self.parse(html)
        normalized = self.normalize(parsed)
        normalized["timestamp"] = datetime.utcnow().isoformat()
        normalized["provider"] = self.provider
        return normalized
