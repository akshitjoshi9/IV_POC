from pydantic import BaseModel, field_serializer
from uuid import UUID
from typing import Optional, List
from datetime import datetime, timezone
from common.utils import PaginationMeta
from conversation.constant import FeedbackReactionsConstants


class FeedbackRead(BaseModel):
    id: UUID
    message_id: UUID
    reactions: Optional[FeedbackReactionsConstants] = None
    created_at: datetime
    updated_at: datetime
    is_active: bool

    class Config:
        from_attributes = True


class FeedbackMessagePayload(BaseModel):
    feedback: Optional[str] = None
    reactions: Optional[FeedbackReactionsConstants] = None  
    payload: FeedbackRead

    class Config:
        from_attributes = True


class MessageResponsePayload(BaseModel):
    """ Schema for the response of message object """

    id: UUID
    parent_id: Optional[UUID]
    role: str
    content: Optional[str]
    status: str
    sources: Optional[List[str]] = None
    feedback: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

    @field_serializer("created_at")
    def serialize_created_at(self, dt: datetime, _info):
        # Always return ISO 8601 UTC
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.isoformat()


class MessageResponse(BaseModel):
    """ Schema for response for the retreive of message """

    message: str
    status: bool
    status_code: Optional[int] = None
    data: List[MessageResponsePayload]
    pagination: PaginationMeta

    class Config:
        from_attributes = True
