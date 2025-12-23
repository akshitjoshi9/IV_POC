from fastapi import APIRouter
from conversation.messages import UserAuthMessages
from common.response import success_response


router = APIRouter()

@router.post("/logout")
def logout():
    """User logout API"""

    return success_response(UserAuthMessages.SUCCESSFULLY_LOGGED_OUT)
