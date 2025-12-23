from sqlmodel import select
from fastapi import HTTPException
from sqlalchemy.orm import selectinload

from typing import Any, List
from core.db import get_session_ml_engine
from common.messages import CommonMessages


def category_dropdown_handler(model, filter_by: List[Any]):
    """
    Returns active categories with their active subcategories based on filters. 
    Raises 404 if no matching records are found.
    """

    session_generator = get_session_ml_engine()
    session = next(session_generator)

    try:
        # Use selectionload to eagerly load the subcategory relationship
        statement = (
            select(model)
            .where(*filter_by)
            .options(selectinload(model.subcategory))
        )
        results = session.exec(statement).all()

        if not results:
            raise HTTPException(status_code=404, detail=CommonMessages.RECORD_NOT_FOUND)

        data = []
        for record in results:
            data.append({
                "category": record.name,
                "subCategory": [
                    {"id": sub.id, "name": sub.name}
                    for sub in record.subcategory
                    if sub.is_active
                ]
            })

        return {
            "message": CommonMessages.RECORD_RETRIEVED_SUCCESSFULLY,
            "status_code": 200,
            "status": True,
            "data": data
        }
    finally:
        try:
            next(session_generator)
        except StopIteration:
            pass
