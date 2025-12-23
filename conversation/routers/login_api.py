from datetime import timedelta
from fastapi import APIRouter, Depends, status
from sqlmodel import select
from sqlmodel import Session
from core.models import User
from conversation.schemas import UserLoginRequest
from core.auth import verify_password, create_access_token, create_refresh_token
from core.db import get_session_ml_engine
from conversation.messages import UserAuthMessages
from common.response import success_response, error_response


router = APIRouter()

@router.post("/login")
def login(data: UserLoginRequest, session: Session = Depends(get_session_ml_engine)):
    """User login API"""

    user = session.exec(select(User).where(User.email == data.email)).first()

    if not user or not verify_password(data.password, user.hashed_password):
        return error_response(UserAuthMessages.INVALID_EMAIL_OR_PASSWORD, status.HTTP_401_UNAUTHORIZED)

    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    response_payload = {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user_id": str(user.id),
        "email": user.email,
        "name": f"{user.first_name} {user.last_name}" if user.first_name else None
    }

    return success_response(UserAuthMessages.SUCCESSFULLY_LOGGED_IN, payload=response_payload)
