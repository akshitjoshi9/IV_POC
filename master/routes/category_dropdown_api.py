from fastapi import APIRouter

from uuid import UUID
from core.models import CategoryMaster
from master.services.category_dropdown_handler import category_dropdown_handler
from master.schemas import CategoryDropdownResponse


router = APIRouter()

@router.get("/category/dropdown", tags=["Dropdown"], response_model=CategoryDropdownResponse)
def category_dropdown(country_id: UUID):
    """
    This route returns the category values with it's subcategories(id, name) based on requested country_id.
    """

    return category_dropdown_handler(
        model=CategoryMaster,
        filter_by=[
            CategoryMaster.is_active == True,
            CategoryMaster.country_id == country_id
        ]
    )
