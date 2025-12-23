import uuid
from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List


class MessageCreateRequest(BaseModel):
    """ Schema for message creation request """

    role: str
    content: str
    thread_id: Optional[uuid.UUID] = None
    country_id: Optional[uuid.UUID] = None
    sub_category_id: Optional[uuid.UUID] = None
    name: Optional[str] = None

    class Config:
        from_attributes = True


class MessageCreateResponsePayload(BaseModel):
    """ Schema for message creation response of assistant """

    id: uuid.UUID
    assistant_id: uuid.UUID
    thread_id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True


class MessageCreateResponse(BaseModel):
    """ Schema for the response of thread api """

    message: str
    status: bool
    status_code: int
    payload: Optional[MessageCreateResponsePayload]

    class Config:
        from_attributes = True
