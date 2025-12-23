import asyncio
import backoff
from loguru import logger
from langchain_community.document_loaders import PlaywrightURLLoader
from sqlalchemy import select
from core.models import ScrapedPage


class WebScrapService:
    def __init__(self, max_concurrent_scrapes: int = 5):
        self.semaphore = asyncio.Semaphore(max_concurrent_scrapes)

    @backoff.on_exception(backoff.expo, Exception, max_tries=3)
    async def _load_url(self, url: str):
        async with self.semaphore:
            try:
                logger.info(f"[Scraper] Starting scrape: {url}")
                loader = PlaywrightURLLoader(urls=[url])
                documents = await loader.aload()
                return documents
            except Exception as e:
                logger.warning(f"[Scraper] Failed {url}: {e}")
                return []


    async def scrape_urls(self, urls, country, session):
        tasks = [self._load_url(url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        all_docs = []
        for url, result in zip(urls, results):
            if isinstance(result, Exception):
                logger.warning(f"[Scraper] Skipped {url} due to error: {result}")
                continue

            if not result:
                logger.warning(f"[Scraper] No content scraped for {url}")
                continue

            all_docs.extend(result)

            exists = session.exec(
                select(ScrapedPage).where(
                    ScrapedPage.url == url, ScrapedPage.country_id == country.id
                )).scalars().all()

            if not exists:
                page = ScrapedPage(url=url, country_id=country.id)
                session.add(page)
                try:
                    session.commit()
                    logger.info(f"[Scraper] Added new URL to DB: {url}")
                except Exception as e:
                    session.rollback()
                    logger.error(f"[Scraper] DB insert failed for {url}: {e}")

        logger.info(f"[Scraper] Completed scraping. Total documents: {len(all_docs)}")
        return all_docs
