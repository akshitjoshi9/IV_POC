from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Header
from fastapi.responses import StreamingResponse
from uuid import UUID
from sqlmodel import Session

from common.auth import get_current_user
from conversation.messages import ThreadMessages
from core.db import get_session_ml_engine
from conversation.services import ChatExportService
from conversation.validators import validate_active_user, validate_active_thread


router = APIRouter()

@router.get("/{thread_id}/export", response_class=StreamingResponse)
def export_chat_pdf(
    thread_id: UUID,
    message_id: Optional[UUID] = None,
    client_timezone: str = Header("UTC", alias="client-timezone"),
    user: dict = Depends(get_current_user),
    db_ml_engine: Session = Depends(get_session_ml_engine),
):
    """ Export all messages of a thread as PDF. """

    user_id = user.get("sub")
    validate_active_user(user_id, db_ml_engine)
    validate_active_thread(thread_id, user_id, db_ml_engine)

    service = ChatExportService(db_ml_engine, client_timezone)
    pdf_stream, file_name = service.generate_chat_pdf(thread_id, message_id)

    if not pdf_stream:
        raise HTTPException(status_code=404, detail=ThreadMessages.NO_MESSAGE_IN_THREAD)

    return StreamingResponse(
        pdf_stream,
        status_code=status.HTTP_200_OK,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{file_name}"'},
    )
