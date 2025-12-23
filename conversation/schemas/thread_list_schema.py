from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from uuid import UUID

from common.utils import PaginationMeta


class ThreadResponsePayload(BaseModel):
    """ Schema for response of the thread object  """

    id: UUID
    name: Optional[str] = None
    is_active: bool
    subcategory_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ThreadListResponsePayload(BaseModel):
    data: List[ThreadResponsePayload]
    pagination: PaginationMeta

    class Config:
        from_attributes = True

class ThreadListResponse(BaseModel):
    """Schema for the response of thread list API with flattened structure."""

    message: str
    status: bool
    status_code: int
    data: List[ThreadResponsePayload]
    pagination: PaginationMeta

    class Config:
        from_attributes = True
