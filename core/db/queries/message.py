from loguru import logger
from sqlalchemy import true
from sqlmodel import select
from common.response import error_response
from core.models import Message, Thread, CountryMaster, CategoryMaster, SubCategoryMaster
from conversation.constant import MessageStatusConstants, MessageRoleConstants
from conversation.messages import ConversionMessages
from uuid import uuid4

def create_thread(body, user, db_engine):
    thread = Thread(
        id=uuid4(),
        country_id=body.country_id,
        subcategory_id=body.sub_category_id,
        name=body.name,
        user_id=user
    )
    db_engine.add(thread)
    db_engine.commit()
    db_engine.refresh(thread)

    logger.info(ConversionMessages.SUCCESS_THREAD_CREATE.format(thread_id=thread.id))
    return thread


def store_messages(body, db_engine):

    message = Message(
        role=body.role,
        content=body.content,
        thread_id=body.thread_id,
        status=MessageStatusConstants.SUCCESS
    )
    assistant_message = Message(
        role=MessageRoleConstants.ASSISTANT,
        parent_id=message.id,
        thread_id=body.thread_id,
        status=MessageStatusConstants.PENDING
    )

    db_engine.add(message)
    db_engine.add(assistant_message)
    db_engine.commit()
    db_engine.refresh(message)
    db_engine.refresh(assistant_message)

    logger.info(f"Message {message.id} and assistant message {assistant_message.id} stored in db successfully")

    return message, assistant_message


def store_assistant_response(result, assistant_message, db_ml_engine, sources, status):
    """ Method to store the llm response in the database """

    message = db_ml_engine.get(Message, assistant_message.id)

    if not message:
        logger.error(f"Message {assistant_message.id} not found")
        return error_response(status_code=404, message="Message not found")

    message.content = result
    message.sources = sources
    if status:
        message.status = MessageStatusConstants.SUCCESS
    else:
        message.status = MessageStatusConstants.FAILED

    db_ml_engine.commit()
    db_ml_engine.refresh(message)

    logger.info(f"Message {message.id} stored in db successfully")
    return None


def get_message(thread_id, message_id, db_ml_engine):
    """ Method to fetch a specific message """

    message = db_ml_engine.exec(
        select(Message).where(
            (Message.thread_id == thread_id) & (Message.id == message_id)
        )
    ).first()

    if not message:
        logger.error(f"Message {message_id} not found")
        return error_response(status_code=404, message="Message not found")

    logger.info(f"Message {message_id} for thread {thread_id} fetched from db successfully")

    return message


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


def get_country(country_id, db_ml_engine):
    """ Method to fetch a specific country """

    country = db_ml_engine.exec(
        select(CountryMaster).where(CountryMaster.id == country_id)
    ).first()

    if not country:
        logger.error(f"Message {country} not found")
        return error_response(status_code=404, message="Message not found")

    logger.info(f"Country {country.name} fetched from db successfully")

    return country

def get_category(subcategory_id, db_ml_engine):
    """ Method to fetch a specific category based on subcategory id """

    sab_category = db_ml_engine.exec(
        select(SubCategoryMaster).where(SubCategoryMaster.id == subcategory_id)
    ).first()

    if not sab_category:
        logger.error("Subcategory not found")
        return error_response(status_code=404, message="Subcategory not found")

    category = db_ml_engine.exec(
        select(CategoryMaster).where(CategoryMaster.id == sab_category.category_id)
    ).first()

    if not category:
        logger.error("Category not found")
        return error_response(status_code=404, message="Category not found")

    logger.info(f"Category {category.name} fetched from db successfully")
    return category