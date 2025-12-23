# utils/pagination.py
from sqlmodel import select, func, Session
from sqlalchemy import and_
from typing import Type, Optional, Dict, Any, List, Tuple
from common.utils import PaginationMeta
from core.config import settings


def paginate_query(
    session: Session,
    model: Type,
    page: int = 1,
    page_size: int = settings.DEFAULT_PAGE_SIZE,
    filters: Optional[List[Any]] = None
) -> Tuple[List[Dict[str, Any]], PaginationMeta]:

    offset = (page - 1) * page_size
    base_query = select(model.id, model.name)
    if filters:
        base_query = base_query.where(and_(*filters))

    count_query = select(func.count()).select_from(model)
    if filters:
        count_query = count_query.where(and_(*filters))

    total_entries = session.exec(count_query).one()
    records = session.exec(base_query.offset(offset).limit(page_size)).all()
    total_pages = (total_entries + page_size - 1) // page_size

    pagination = PaginationMeta(
        page_size=page_size,
        total_pages=total_pages,
        current_page=page,
        total_entries=total_entries,
        next=page + 1 if page < total_pages else None,
        previous=page - 1 if page > 1 else None
    )

    return records, pagination
