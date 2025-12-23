from uuid import UUID
from loguru import logger
from fastapi import HTTPException
from sqlalchemy.orm import Session

from core.db.queries import get_user, get_thread


def validate_active_user(user_id: int, db: Session):
    """ Validator to validate active user based on user id """

    user = get_user(user_id, db)
    if not user:
        logger.info(f"User {user_id} not found")
        raise HTTPException(status_code=404, detail="Active user not found")

    logger.info(f"User {user_id} fetched from db successfully")

    return user


def validate_active_thread(thread_id: UUID, user_id: int, db: Session):
    """ Validator to validate active thread based on thread id """

    thread = get_thread(thread_id, user_id, db)
    if not thread:
        logger.info(f"Thread {thread_id} not found")
        raise HTTPException(status_code=404, detail="Thread not found")

    logger.info(f"Thread {thread_id} fetched from db successfully")

    return thread