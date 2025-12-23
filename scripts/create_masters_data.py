import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import datetime, timezone
from sqlmodel import select
from common.messages import CommonMessages
from core.models import CountryMaster, CategoryMaster, SubCategoryMaster
from core.db import get_session_ml_engine


def seed_data():
    # Manually get session from the generator
    session = next(get_session_ml_engine())
    
    # Step 1: Check/Add Country
    uk_country = session.exec(
        select(CountryMaster).where(CountryMaster.name == "United Kingdom")
    ).first()

    if not uk_country:
        uk_country = CountryMaster(
            name="United Kingdom",
            is_active=True,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        session.add(uk_country)
        session.commit()
        session.refresh(uk_country)

    # Step 2: Check/Add Category
    clinical_trial_category = session.exec(
        select(CategoryMaster).where(
            CategoryMaster.name == "Clinical Trial",
            CategoryMaster.country_id == uk_country.id
        )
    ).first()

    if not clinical_trial_category:
        clinical_trial_category = CategoryMaster(
            name="Clinical Trial",
            country_id=uk_country.id,
            is_active=True,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        session.add(clinical_trial_category)
        session.commit()
        session.refresh(clinical_trial_category)

    # Step 3: Check/Add Subcategories
    subcategory_names = ["Legal Basis", "Periodic Aggregated", "Expedited"]

    for name in subcategory_names:
        existing_subcategory = session.exec(
            select(SubCategoryMaster).where(
                SubCategoryMaster.name == name,
                SubCategoryMaster.category_id == clinical_trial_category.id
            )
        ).first()

        if not existing_subcategory:
            subcategory = SubCategoryMaster(
                name=name,
                category_id=clinical_trial_category.id,
                is_active=True,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            )
            session.add(subcategory)

    session.commit()
    print(CommonMessages.DATA_ADDED_SUCCESSFULLY)


if __name__ == "__main__":
    seed_data()
