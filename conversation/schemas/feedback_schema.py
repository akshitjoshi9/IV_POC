from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime
from enum import Enum
from conversation.constant import FeedbackReactionsConstants


class FeedbackCreateUpdate(BaseModel):
    """ Verifies request body for creating and updating feedback. """
    message_id: Optional[uuid.UUID] = None
    reactions: Optional[FeedbackReactionsConstants] = None


class FeedbackRead(BaseModel):
    id: uuid.UUID
    message_id: uuid.UUID
    reactions: Optional[FeedbackReactionsConstants]
    created_at: datetime
    updated_at: datetime
    is_active: bool

    class Config:
        from_attributes = True


class FeedbackUpdateResponse(BaseModel):
    message: str
    status: bool
    status_code: int
    payload: FeedbackRead

    class Config:
        from_attributes = True
