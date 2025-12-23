from pydantic import BaseModel, field_validator
import re
from conversation.messages import UserAuthMessages


class UserLoginRequest(BaseModel):
    """This schema validates the request body of login api."""

    email: str
    password: str

    @field_validator("email")
    @classmethod
    def validate_email_not_blank(cls, value):
        if not value or not str(value).strip():
            raise ValueError(UserAuthMessages.EMAIL_CANNOT_BE_BLANK)

        # Email regex validation
        email_regex = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
        if not re.match(email_regex, value):
            raise ValueError(UserAuthMessages.INVALID_EMAIL_FORMAT)

        return value

    @field_validator("password")
    @classmethod
    def validate_password_not_blank(cls, value):
        if not value or not str(value).strip():
            raise ValueError(UserAuthMessages.PASSWORD_CANNOT_BE_BLANK)
        return value


class TokenResponse(BaseModel):
    """This schema returns the response for login api."""

    access_token: str
    token_type: str = "bearer"
    user_id: str
    email: str
    name: str | None = None
