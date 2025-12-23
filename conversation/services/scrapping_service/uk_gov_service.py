import requests
import feedparser
from .base_scraper_service import BaseScraper


class GovUKScrapperService(BaseScraper):
    feeds = [
        "https://www.gov.uk/search/news-and-communications.atom",
        "https://www.gov.uk/search/guidance-and-regulation.atom",
    ]

    organisation = "medicines-and-healthcare-products-regulatory-agency"

    @classmethod
    def fetch_feed_links(cls, base_url, all_links):
        """Fetch all links from a single feed with pagination"""
        params = {"organisations[]": cls.organisation, "page": 1}
        while True:
            resp = requests.get(base_url, params=params)
            feed = feedparser.parse(resp.text)

            if not feed.entries:
                break

            for entry in feed.entries:
                all_links.add(entry.link)

            params["page"] += 1

    @classmethod
    def execute(cls) -> list:
        """Run fetching for all feeds"""
        all_links = set()
        for base_url in cls.feeds:
            cls.fetch_feed_links(base_url, all_links)

        return list(all_links)
