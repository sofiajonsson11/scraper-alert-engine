from abc import ABC, abstractmethod


class BaseScraper(ABC):
    """Abstract base class for all weather scrapers."""

    provider = None
    location = None

    def __init__(self, location: str):
        self.location = location

    @abstractmethod
    def fetch(self) -> dict:
        """Fetch, parse, and normalize data. Must return dict with keys: temperature, description, feels_like, url"""
        raise NotImplementedError

    @abstractmethod
    def normalize(self, raw_data: dict) -> dict:
        """Normalize raw scraped data."""
        pass
