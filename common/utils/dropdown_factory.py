# routers/utils/dropdown_factory.py
from fastapi import Query, Depends
from sqlmodel import Session
from typing import Type, Optional, Any, Callable

from common.utils.pagination import paginate_query
from common.utils.id_name_dropdown_schema import StandardResponse, DropdownIDNameResponse
from common.messages import CommonMessages
from core.db import get_session_ml_engine
from core.config import settings


def dropdown_handler(model: Type, filter_by: Optional[Any] = None) -> Callable:
    """
    Factory function to generate dropdown API handlers.
    Returns paginated records with only 'id' and 'name' fields, applying optional filters.
    """

    def _handler(
        session: Session = Depends(get_session_ml_engine),
        page: int = Query(1, ge=1),
        page_size: int = Query(default=settings.DEFAULT_PAGE_SIZE, ge=1, le=settings.MAX_PAGE_SIZE)
    ) -> StandardResponse:

        records, pagination = paginate_query(
            session=session,
            model=model,
            page=page,
            page_size=page_size,
            filters=filter_by
        )

        data = [DropdownIDNameResponse(id=record.id, name=record.name) for record in records]

        return StandardResponse(
            message=CommonMessages.RECORD_RETRIEVED_SUCCESSFULLY,
            status_code=200,
            status=True,
            pagination=pagination,
            data=data
        )

    return _handler
