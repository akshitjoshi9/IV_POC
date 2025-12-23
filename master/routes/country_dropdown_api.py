from fastapi import APIRouter
from common.utils.dropdown_factory import dropdown_handler
from common.utils.id_name_dropdown_schema import StandardResponse
from core.models import CountryMaster


router = APIRouter()

"""
Here, no need to define the dropdown API 
- Defined like below using a factory function, Reason: Reusability and DRY.
- You're using a higher-order function (i.e., dropdown_handler) to generate FastAPI route functions dynamically. 
- This design is: Reusable for many dropdown APIs
ex: here rename the url and model to create new dropdown to retrieve active records with pagination.
"""

# Returns all the active countries in id, name format.
router.get("/country/dropdown", tags=["Dropdown"], response_model=StandardResponse)(
    dropdown_handler(
        model=CountryMaster, 
        filter_by=(CountryMaster.is_active == True)
        )
)
