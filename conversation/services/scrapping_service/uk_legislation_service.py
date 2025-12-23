import time
import requests
import backoff
from bs4 import BeautifulSoup
from .base_scraper_service import BaseScraper
from common.constant import legislation_unused_urls


class UKLegislationScraper(BaseScraper):
    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/118.0 Safari/537.36"
        )
    }
    FORCE_INCLUDED_URL = ["https://www.legislation.gov.uk/en/uksi/2025/538/data.xht?view=snippet&wrap=true",
                          "https://www.legislation.gov.uk/uksi/2024/832/data.xht?view=snippet&wrap=true"]

    @backoff.on_exception(
        backoff.expo,
        requests.exceptions.RequestException,
        max_tries=5,
        jitter=None
    )
    def fetch_page(self, url: str) -> str:
        """Fetch the HTML content of the main page with retry + backoff."""
        try:
            response = requests.get(
                url,
                timeout=(10, 60),
                headers=self.HEADERS
            )
            response.raise_for_status()
            time.sleep(1)  # polite delay
            return response.content
        except requests.exceptions.RequestException as e:
            print(f"Error fetching page: {e}")
            return ""

    def extract_links(self) -> list:
        """Extract and filter unique links from the page."""
        html_content = self.fetch_page(self.main_url)
        if not html_content:
            return []

        soup = BeautifulSoup(html_content, "html.parser")

        unique_links = set()
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if not href:
                continue

            # Skip unwanted links
            if any(x in href for x in [
                "/regulation", "/schedule", "/part", "/annex", "/article", "#",
                "/asp", "/apni", "/eudr", "/eur", "/nia", "/nisi", "nisr",
                "ssi", "/wsi"
            ]):
                continue

            if href in legislation_unused_urls:
                continue

            href = href.rstrip("/") + "/data.xht?view=snippet&wrap=true"
            unique_links.add(href)
        unique_links.update(self.FORCE_INCLUDED_URL)
        return sorted(unique_links)

    def execute(self) -> list:
        """Main method to run the scraper and return links."""
        return self.extract_links()
