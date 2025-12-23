from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, status

from common.auth import get_current_user
from core.db import get_session_ml_engine
from core.models import Feedback
from conversation.schemas import (
    FeedbackRead, FeedbackCreateUpdate, FeedbackUpdateResponse,
    )
from conversation.messages import ConversionMessages


router = APIRouter()

@router.post("/feedback", response_model=FeedbackUpdateResponse)
def add_update_feedback(
    feedback_data: FeedbackCreateUpdate,
    session: Session = Depends(get_session_ml_engine),
    user: dict = Depends(get_current_user) 
):
    user_id = user.get('sub')
    existing_feedback = session.query(Feedback).filter(
        Feedback.message_id == feedback_data.message_id
    ).first()

    if existing_feedback:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ConversionMessages.FEEDBACK_ALREADY_EXISTS
        )

    # Create new feedback
    feedback = Feedback(
        message_id=feedback_data.message_id,
        reactions=feedback_data.reactions,
        user_id=user_id,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    session.add(feedback)

    session.commit()
    session.refresh(feedback)

    return FeedbackUpdateResponse(
        message=ConversionMessages.FEEDBACK_ADDED_SUCCESSFULLY,
        status=True,
        status_code=status.HTTP_200_OK,
        payload=FeedbackRead.model_validate(feedback)  # Converts SQLAlchemy --> Pydantic
    )
