from uuid import UUID
from fastapi import HTTPException
from sqlmodel import select
from sqlalchemy import true, desc
from sqlalchemy.orm import Session
from conversation.messages import ThreadMessages
from conversation.schemas import ThreadNameUpdateRequest
from core.models import Thread, Message


def get_all_threads(user_id, country_id):
    """
    Return query to fetch all active threads for a specific workspace and user
    """

    return select(Thread).where(
        Thread.user_id == user_id,
        Thread.country_id == country_id,
        Thread.is_active == true()
    ).order_by(desc(Thread.created_at))


def get_thread(thread_id, user_id, session):
    """ Get a thread object by thread id """

    thread = session.exec(
        select(Thread).where(
            Thread.id == thread_id,
            Thread.is_active == true(),
            Thread.user_id == user_id
        )
    ).first()

    return thread


def delete_thread_with_message(user_id: UUID, thread_id: UUID, db: Session) -> Thread:
    """
    Ensure the thread exists and is active before deleting it along with all its associated messages.
    """

    thread = db.query(Thread).filter(
    Thread.user_id == user_id, Thread.id == thread_id, Thread.is_active == True
    ).first()

    if not thread:
        raise HTTPException(status_code=404, detail=ThreadMessages.THREAD_NOT_FOUND)

    db.delete(thread)
    db.commit()

    return True


def update_thread_name_query(user_id: UUID, data: ThreadNameUpdateRequest, db: Session) -> Thread:
    """Validate and update the thread name."""

    thread = db.query(Thread).filter(
        Thread.user_id == user_id, Thread.id == data.thread_id, Thread.is_active == True
    ).first()

    if not thread:
        raise HTTPException(status_code=404, detail=ThreadMessages.THREAD_NOT_FOUND)

    thread.name = data.name
    db.commit()
    db.refresh(thread)

    return thread
