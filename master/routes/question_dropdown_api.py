from fastapi import APIRouter, Depends, Query
from sqlmodel import Session
from typing import Optional
from uuid import UUID
from common.utils.id_name_dropdown_schema import StandardResponse
from common.utils.pagination import paginate_query
from common.messages import CommonMessages

from core.db import get_session_ml_engine
from core.models import QuestionMaster
from core.config import settings


router = APIRouter()

@router.get("/question/dropdown", tags=["Dropdown"], response_model=StandardResponse)
def question_dropdown(
    subcategory_id: UUID,
    page: int = Query(1, ge=1),
    page_size: int = Query(settings.DEFAULT_PAGE_SIZE, ge=1, le=settings.MAX_PAGE_SIZE),
    search: Optional[str] = Query(None, description="Search keyword for question name"),
    session: Session = Depends(get_session_ml_engine)
):
    """
    This route returns the questions (id, name) based on requested subcategory_id.
    """
    filters = [
        QuestionMaster.is_active == True,
        QuestionMaster.subcategory_id == subcategory_id
    ]

    if search:
        filters.append(QuestionMaster.name.ilike(f"%{search}%"))
    data, pagination = paginate_query(
        session=session,
        model=QuestionMaster,
        page=page,
        page_size=page_size,
        filters=filters
    )
    return {
        "message": CommonMessages.RECORD_RETRIEVED_SUCCESSFULLY,
        "status_code": 200,
        "status": True,
        "pagination": pagination,
        "data": data
    }
