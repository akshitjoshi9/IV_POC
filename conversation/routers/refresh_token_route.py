from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlmodel import Session, select

from common.messages import CommonMessages
from common.response import success_response
from core.config import settings
from core.db import get_session_ml_engine
from core.auth import create_access_token
from core.models import User
from core.validators import validate_active_user

from conversation.schemas import RefreshTokenRequest


router = APIRouter()

@router.post("/refresh-token")
def refresh_token(request: RefreshTokenRequest, session: Session = Depends(get_session_ml_engine)):
    try:
        payload = jwt.decode(request.refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(status_code=401, detail=CommonMessages.INVALID_REFRESH_TOKEN)

        user = validate_active_user(user_id, session)
        access_token = create_access_token(data={"sub": str(user.id)})

        response_payload = {
            "access_token": access_token,
            "refresh_token": request.refresh_token,
            "token_type": "bearer",
            "user_id": str(user.id),
            "email": user.email,
            "name": f"{user.first_name} {user.last_name}" if user.first_name else None
        }

        return success_response(CommonMessages.ACCESS_TOKEN_REFRESHED, payload=response_payload)

    except JWTError:
        raise HTTPException(status_code=401, detail=CommonMessages.INVALID_REFRESH_TOKEN)
