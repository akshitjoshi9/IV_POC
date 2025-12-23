from fastapi_pagination import Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlmodel import Session
from sqlmodel import select
from sqlalchemy import asc
from sqlalchemy.orm import selectinload
from uuid import UUID
import pytz

from common.utils import build_pagination_meta
from common.messages import CommonMessages
from common.response import error_response
from common.services import convert_to_user_timezone

from core.models import Message
from conversation.schemas import MessageResponsePayload
from conversation.schemas import (
    MessageResponsePayload, MessageResponse
    )
from core.validators import validate_active_thread, validate_active_user
from loguru import logger


def get_thread_messages(
    thread_id: UUID,
    user_id: UUID,
    params: Params,
    db_ml_engine: Session,
    user_tz: pytz.BaseTzInfo,
) -> MessageResponse:
    """
        Retrieve paginated messages for a thread after user and thread validation.
    """

    # Validation
    validate_active_user(user_id, db_ml_engine)
    validate_active_thread(thread_id, user_id, db_ml_engine)

    # Query messages with feedback relationship
    query = (
        select(Message)
        .where(Message.thread_id == thread_id)
        .options(selectinload(Message.feedback))
        .order_by(asc(Message.created_at))
    )

    # Pagination
    page = paginate(db_ml_engine, query, params)

    messages = []
    for item in page.items:
        # Convert created_at to user timezone
        created_at_user_tz = convert_to_user_timezone(item.created_at, user_tz)
        payload = MessageResponsePayload(
            id=item.id,
            parent_id=item.parent_id,
            role=item.role,
            content=item.content,
            status=item.status,
            sources=item.sources,
            feedback=item.feedback.reactions if item.feedback else None,
            created_at=created_at_user_tz,
        )
        messages.append(payload)

    if not messages:
        logger.bind(thread_id=thread_id).error(CommonMessages.RECORD_NOT_FOUND)
        return error_response(CommonMessages.RECORD_NOT_FOUND, status_code=404)

    logger.bind(thread_id=thread_id).info(CommonMessages.RECORD_RETRIEVED_SUCCESSFULLY)
    pagination = build_pagination_meta(params, page)

    return MessageResponse(
        message=CommonMessages.RECORD_RETRIEVED_SUCCESSFULLY,
        status=True,
        status_code=200,
        data=messages,
        pagination=pagination
    )
