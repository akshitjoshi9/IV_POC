from loguru import logger
from sqlalchemy import select

from core.db.session import get_session_ml_engine
from core.models import CountryMaster
from conversation.services import (
    WebScrapService, DocumentFormatting, EmbeddingVectorStore, UKLegislationScraper, GovUKScrapperService
)

SCRAPER_REGISTRY = {
    "https://www.legislation.gov.uk/uksi/2012/1916/data.xht?view=snippet&wrap=true": UKLegislationScraper,
    # "https://www.gov.uk/": GovUKScrapperService
}

async def web_scrapping_task():
    logger.info("Web scrapping task started")
    session_generator = get_session_ml_engine()
    session = next(session_generator)

    scraper = WebScrapService()
    formatter = DocumentFormatting()
    embedder = EmbeddingVectorStore()
    try:
        countries = session.exec(
            select(CountryMaster).where(CountryMaster.is_active == True)
        ).scalars().all()

        for country in countries:
            main_urls = [ds.link for ds in country.datasource if ds.link]

            for url in main_urls:
                scraper_cls = SCRAPER_REGISTRY.get(url)
                if not scraper_cls:
                    logger.warning(f"No scraper implemented for {url}")
                    continue

                sub_urls = scraper_cls(country=country, main_url=url).execute()
                if not sub_urls:
                    logger.warning(f"No URLs for country: {country.name}")
                    continue

                documents = await scraper.scrape_urls(sub_urls, country, session)
                formatted_docs = formatter.format_docs_with_metadata(documents)
                _, collection = embedder.embedding_vector_store_service(
                    formatted_docs, country=country.name, main_url=url
                )
                logger.info(f"Stored in Milvus collection: {collection}")
                logger.info(f"Documents embedded and stored for {country.name}. Total: {len(formatted_docs)}")

    except Exception as e:
        logger.error(f"Error in web scraping task: {e}")
    finally:
        session.close()
        logger.info("Session closed")
