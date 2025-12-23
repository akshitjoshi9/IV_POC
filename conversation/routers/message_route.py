from uuid import UUID
from fastapi_pagination import Params
from fastapi import APIRouter, BackgroundTasks, Depends, status, Header
from sqlmodel import Session

from common.rag import MainService
from common.auth import get_current_user
from common.response import error_response
from common.services import get_user_timezone
from conversation.messages import ConversionMessages
from conversation.schemas import (
    MessageCreateRequest, MessageCreateResponse, MessageCreateResponsePayload, MessageResponse
    )
from core.db.session import get_session_ml_engine
from core.validators import validate_active_thread, validate_active_user
from core.db.queries import store_messages, create_thread, get_message
from conversation.services import StreamMessageService, get_thread_messages
from loguru import logger
import pytz


router = APIRouter()

@router.post("/message")
def create_message(
        body: MessageCreateRequest,
        background_tasks: BackgroundTasks,
        user: dict = Depends(get_current_user),
        db_engine: Session = Depends(get_session_ml_engine),
        user_tz: pytz.BaseTzInfo = Depends(get_user_timezone)
):
    """ Method to create a new message in the thread of User and Assistant messages """
    user_id = user.get('sub')
    if body.thread_id is None:
        missing_fields = not all([body.country_id, body.sub_category_id, body.name])
        if missing_fields:
            logger.error(ConversionMessages.REQUIRED_FIELD_IN_MESSAGE)
            return error_response(ConversionMessages.REQUIRED_FIELD_IN_MESSAGE, status_code=404)

        thread = create_thread(body, user_id, db_engine)
        body.thread_id = thread.id

    user_message, assistant_message = store_messages(body, db_engine)

    if not user_message or not assistant_message:
        logger.error(ConversionMessages.ERROR_MESSAGE_CREATE)
        return error_response(ConversionMessages.ERROR_MESSAGE_CREATE, status_code=404)

    background_tasks.add_task(MainService().main_executor, body,
                              user_message, assistant_message, db_engine)

    return MessageCreateResponse(
        message=ConversionMessages.SUCCESS_MESSAGES_CREATE,
        status=True,
        status_code=status.HTTP_200_OK,
        payload=MessageCreateResponsePayload(
            id=user_message.id,
            assistant_id=assistant_message.id,
            thread_id=body.thread_id,
            created_at=user_message.created_at.astimezone(user_tz)
        )
    )


@router.get("/{thread_id}/messages", response_model=MessageResponse)
def list_messages(
    thread_id: UUID,
    user: dict = Depends(get_current_user),
    params: Params = Depends(),
    db_ml_engine: Session = Depends(get_session_ml_engine),
    user_tz: pytz.BaseTzInfo = Depends(get_user_timezone),
    ):
    """Get question-answer messages for a specific thread"""

    user_id = user.get("sub")
    response_data = get_thread_messages(
        thread_id=thread_id,
        user_id=user_id,
        params=params,
        db_ml_engine=db_ml_engine,
        user_tz=user_tz,
    )
    return response_data


@router.get("/{thread_id}/stream/{message_id}/")
def stream(
        message_id: UUID,
        thread_id: UUID,
        client_timezone: str = Header("UTC", alias="client-timezone"),
        user: dict = Depends(get_current_user),
        db_engine: Session = Depends(get_session_ml_engine)
):
    """ Stream the assistant message """

    user_id = user.get('sub')
    validate_active_user(user_id, db_engine)
    validate_active_thread(thread_id, user_id, db_engine)
    message = get_message(thread_id, message_id, db_engine)
    if not message:
        logger.bind(thread_id=thread_id).error(ConversionMessages.ERROR_MESSAGE_RETRIEVE)
        return error_response(ConversionMessages.ERROR_MESSAGE_RETRIEVE, status_code=404)

    logger.bind(thread_id=thread_id, message_id=message_id).info(ConversionMessages.SUCCESS_MESSAGE_STREAM)

    return StreamMessageService(message_id, user_timezone=client_timezone).get_streaming_response()
