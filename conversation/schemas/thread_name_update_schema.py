from uuid import UUID
from pydantic import BaseModel


class ThreadNameUpdateRequest(BaseModel):
    thread_id: UUID
    name: str


class ThreadNameUpdateResponse(BaseModel):
    """This is update thread name response schema."""

    message: str
    status: bool
    status_code: int
    payload: dict
