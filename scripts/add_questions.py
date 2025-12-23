import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import datetime, timezone
from sqlmodel import select
from common.constant import QUESTIONS_DATA
from common.messages import CommonMessages
from core.models import CountryMaster, SubCategoryMaster, QuestionMaster
from core.db import get_session_ml_engine

from loguru import logger


def seed_questions(country_name: str = "United Kingdom"):
    """ This function add sub-category new questions to question master."""

    session = next(get_session_ml_engine())
    country = session.exec(select(CountryMaster).where(CountryMaster.name == country_name)).first()
    if not country:
        logger.warning(f"Country '{country_name}' not found.")
        return
    
    for subcategory_name, questions in QUESTIONS_DATA.items():
        # Get subcategory
        subcategory = session.exec(
            select(SubCategoryMaster)
            .where(SubCategoryMaster.name == subcategory_name)
            .where(SubCategoryMaster.category_id != None)
        ).first()

        if not subcategory:
            logger.warning(f"Subcategory '{subcategory_name}' not found.")
            continue

        for question_text in questions:
            # Check for duplicate
            existing_question = session.exec(
                select(QuestionMaster).where(
                    QuestionMaster.name == question_text,
                    QuestionMaster.country_id == country.id,
                    QuestionMaster.subcategory_id == subcategory.id
                )
            ).first()

            if existing_question:
                logger.info(f"Skipping duplicate: {question_text}")
                continue

            # Create new QuestionMaster entry
            question = QuestionMaster(
                name=question_text,
                country_id=country.id,
                subcategory_id=subcategory.id,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
                is_active=True
            )
            session.add(question)

    session.commit()
    logger.success(CommonMessages.DATA_ADDED_SUCCESSFULLY)


if __name__ == "__main__":
    seed_questions()