from fastapi import FastAPI
from fastapi_pagination import add_pagination
from contextlib import asynccontextmanager

from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from pydantic import ValidationError

from common.services.exception_handler_service import (validation_exception_handler, http_exception_handler,
                                               pydantic_exception_handler,)
from conversation.routers import (
    login_api, logout_api, message_route, thread_route, run_scrap_route, refresh_token_route,
    message_feed_back_route, export_route,
    )
from core.scheduler import start_scheduler
from master.routes import country_dropdown_api, category_dropdown_api, question_dropdown_api


@asynccontextmanager
async def lifespan(app: FastAPI):
    # start_scheduler()
    yield

app = FastAPI(lifespan=lifespan)
add_pagination(app)

# Register common custom handlers
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(ValidationError, pydantic_exception_handler)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# User Authentication
app.include_router(login_api.router, prefix="/user", tags=["Auth"])
app.include_router(logout_api.router, prefix="/user", tags=["Auth"])
app.include_router(refresh_token_route.router, prefix="/user", tags=["Auth"])

# Masters
app.include_router(country_dropdown_api.router, prefix="/master", tags=["Auth"])
app.include_router(category_dropdown_api.router, prefix="/master", tags=["Dropdown"])
app.include_router(question_dropdown_api.router, prefix="/master", tags=["Dropdown"])

# Thread/Message
app.include_router(message_route.router, prefix="/thread", tags=["Message"])
app.include_router(thread_route.router, prefix="/thread", tags=["Thread"])
app.include_router(export_route.router, prefix="/thread", tags=["Thread"])
app.include_router(message_feed_back_route.router, prefix="/thread", tags="Message")

# Run Web Scraping
app.include_router(run_scrap_route.router, prefix="/scrap", tags=["Scraping"])
