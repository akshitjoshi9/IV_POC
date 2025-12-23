from uuid import UUID
from sqlmodel import Session
from fastapi import APIRouter, Depends, Query, status
from fastapi_pagination import Params
from fastapi_pagination.ext.sqlmodel import paginate
from loguru import logger

from common.utils import build_pagination_meta
from common.auth import get_current_user

from conversation.schemas import (
    ThreadResponsePayload, ThreadListResponse, ThreadDeleteResponse, ThreadNameUpdateRequest,
    ThreadNameUpdateResponse,
    )
from conversation.schemas import ThreadResponsePayload
from conversation.messages import ThreadMessages
from core.db.session import get_session_ml_engine
from core.db.queries import get_all_threads, delete_thread_with_message, update_thread_name_query


router = APIRouter()

@router.get("/list", response_model=ThreadListResponse)
def list_thread(
    country_id: UUID = Query(..., description="Country ID from frontend"),
    params: Params = Depends(),
    user: dict = Depends(get_current_user),
    db_ml_engine: Session = Depends(get_session_ml_engine),
    ):
    """Method to get the list of all threads"""

    user_id = user.get("sub")
    # Get threads
    query = get_all_threads(user_id=user_id, country_id=country_id)
    page = paginate(db_ml_engine, query, params)

    if not page.items:
        logger.info(ThreadMessages.THREAD_NOT_FOUND)

    logger.info(ThreadMessages.SUCCESS_THREADS_RETRIEVE)

    pagination = build_pagination_meta(params, page)

    return ThreadListResponse(
        message=ThreadMessages.SUCCESS_THREADS_LIST,
        status_code=status.HTTP_200_OK,
        status=True,
        data=[ThreadResponsePayload.model_validate(thread) for thread in page.items],
        pagination=pagination
        )


@router.delete("/delete", response_model=ThreadDeleteResponse)
def delete_thread(
    thread_id: UUID,
    user: dict = Depends(get_current_user),
    db_ml_engine: Session = Depends(get_session_ml_engine),
    ):
    """Delete a thread with it's related messages by thread ID."""

    user_id = user.get("sub")
    delete_thread_with_message(user_id, thread_id, db_ml_engine)
    logger.bind(thread_id=thread_id).info(ThreadMessages.THREAD_SUCCESSFULLY_DELETED)

    return ThreadDeleteResponse(
        message=ThreadMessages.THREAD_SUCCESSFULLY_DELETED,
        status=True,
        status_code=status.HTTP_200_OK,
        payload={}
    )


@router.put("/update-thread-name", response_model=ThreadNameUpdateResponse)
def update_thread_name(
    data: ThreadNameUpdateRequest,
    user: dict = Depends(get_current_user),
    db_ml_engine: Session = Depends(get_session_ml_engine),
    ):
    """Update the name of a thread."""

    user_id = user.get("sub")
    updated_thread = update_thread_name_query(user_id, data, db_ml_engine)    
    logger.bind(thread_id=data.thread_id).info(ThreadMessages.THREAD_NAME_UPDATED_SUCCESSFULLY)

    return ThreadNameUpdateResponse(
        message=ThreadMessages.THREAD_NAME_UPDATED_SUCCESSFULLY,
        status=True,
        status_code=status.HTTP_200_OK,
        payload={"thread_id": str(updated_thread.id), "name": updated_thread.name}
    )
