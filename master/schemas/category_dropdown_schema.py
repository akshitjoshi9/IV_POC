from typing import List,Optional
from uuid import UUID
from pydantic import BaseModel


class SubCategoryDropdown(BaseModel):
    id: UUID
    name: Optional[str] = None


class CategoryDropdown(BaseModel):
    category: str
    subCategory: List[SubCategoryDropdown]


class CategoryDropdownResponse(BaseModel):
    """
    This returns the actieve category records with respective active sub-categories with id, name.
    """
    message: str
    status_code: int
    status: bool
    data: List[CategoryDropdown]
