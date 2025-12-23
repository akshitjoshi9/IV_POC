from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from pydantic import ValidationError

from common.response import error_response
from common.messages import CommonMessages


app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Custom exception handler for request validation errors.
    Extracts and formats validation error messages, removes unnecessary prefixes,
    and returns a consistent JSON response structure for client-side handling.
    """
    error_details = {}

    for err in exc.errors():
        field = err.get("loc")[-1]
        message = err.get("msg")

        # Clean the "Value error, " prefix if present
        if message.lower().startswith("value error, "):
            message = message[13:].strip()

        error_details[field] = message

    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({
            "status": False,
            "status_code": 422,
            "message": CommonMessages.VALIDATION_ERROR,
            "payload": error_details,
        }),
    )

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """
    Handles general HTTP exceptions raised by Starlette or FastAPI.
    Returns a structured JSON error response with the appropriate HTTP status code and message.
    """

    return error_response(
        message=exc.detail,
        status_code=exc.status_code
    )

@app.exception_handler(ValidationError)
async def pydantic_exception_handler(request: Request, exc: ValidationError):
    """
    Handles internal Pydantic validation errors that occur during model creation 
    or data processing, not directly from incoming API requests.
    """
    return error_response(
        message=CommonMessages.PYDANTIC_VALIDATION_FAILED,
        status_code=422
    )
