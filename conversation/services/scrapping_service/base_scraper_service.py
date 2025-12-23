from abc import ABC, abstractmethod

class BaseScraper(ABC):
    def __init__(self, country, main_url):
        self.country = country,
        self.main_url = main_url

    @abstractmethod
    def execute(self) -> list[dict]:
        """Scrape legislation pages for this country and return structured data"""
        pass
