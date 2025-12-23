import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlmodel import select, Session
from common.messages import CommonMessages
from core.models import CountryMaster, DataSourceMaster
from core.db.session import engine_ml
from master.constant import country_and_data_source


def create_countries_and_datasources():
    """
    This script creates unique countries and associated data sources (links).
    No duplicates are inserted.
    """
    with Session(engine_ml) as db:
        for entry in country_and_data_source:
            country_name = entry["country"].strip()
            links = entry.get("links", [])

            # Check if the country already exists (case-insensitive)
            country = db.exec(
                select(CountryMaster).where(CountryMaster.name.ilike(country_name))
            ).first()

            # If country doesn't exist, create it
            if not country:
                country = CountryMaster(name=country_name)
                db.add(country)
                db.commit()
                db.refresh(country)

            # Add unique data source links for the country
            for link in links:
                link = link.strip()

                # Check if the link already exists for this country
                existing_link = db.exec(
                    select(DataSourceMaster).where(
                        DataSourceMaster.link == link,
                        DataSourceMaster.country_id == country.id,
                    )
                ).first()

                if not existing_link:
                    db.add(DataSourceMaster(link=link, country_id=country.id))

            db.commit()
            print(CommonMessages.DATA_ADDED_SUCCESSFULLY)


if __name__ == "__main__":
    create_countries_and_datasources()
