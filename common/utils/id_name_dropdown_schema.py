# schemas/standard_response.py
from pydantic import BaseModel
from typing import Optional, List, Union
from uuid import UUID


class DropdownIDNameResponse(BaseModel):
    id: UUID
    name: Optional[str] = None


class PaginationMeta(BaseModel):
    page_size: int
    total_pages: int
    current_page: int
    total_entries: int
    next: Optional[int] = None
    previous: Optional[int] = None


class StandardResponse(BaseModel):
    """
    Schema for standard API responses. Includes message, HTTP status code, 
    success flag, and paginated payload data.
    """
    message: str
    status_code: int
    status: bool
    pagination: PaginationMeta
    data: List[DropdownIDNameResponse]
