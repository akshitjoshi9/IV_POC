import asyncio
import json
from loguru import logger

from langchain.schema import BaseMessage
from langchain.schema.messages import messages_to_dict, messages_from_dict
from langchain_core.chat_history import BaseChatMessageHistory
from pymongo import MongoClient

from common.redis import RedisWrapper
from core.config import settings


class ConversationMemoryStorage(BaseChatMessageHistory):
    """
    This class will be use to store and load the thread wise chat history for the conversation buffer memory
    """

    def __init__(self, session_id: str, memory):
        self.redis_wrapper = RedisWrapper(db=settings.REDIS_MEMORY_DB)
        self.session_id = session_id
        self.connection = settings.MONGODB_URL
        self.client = MongoClient(self.connection)
        self.collection = self.client[settings.MONGODB_DB][settings.MONGODB_COLLECTION]
        self.memory = memory
        self.load_memory_conversations()

    def add_message(self, message: BaseMessage) -> None:
        """ this service use to store thread wise conversation """
        self.collection.update_one(
            {"session_id": self.session_id},
            {"$push": {"messages": {"$each": messages_to_dict([message])}}}
        )

        logger.info(f"Message added to session: {self.session_id} in DB")

    def redis_add_message(self, message):
        """ To store the messages into redis cache """
        cache_data = self.redis_wrapper.get(self.session_id)
        cache_data["messages"].extend(messages_to_dict([message]))
        self.redis_wrapper.setex(self.session_id, 1800, json.dumps(cache_data))
        logger.info(f"Message added to session: {self.session_id} in redis")

    async def store_message_db_and_cache(self, message):
        """This service will store message in DB and cache at same time """

        await asyncio.gather(
            asyncio.to_thread(self.add_message, message),
            asyncio.to_thread(self.redis_add_message, message)
        )
        logger.info("Messages stored successfully in DB and cache memory")

    def load_memory_conversations(self):
        """ This service always reload conversation into  buffer memory """

        cache_data = self.redis_wrapper.get(self.session_id)
        if not cache_data:
            db_data = self.collection.find_one({"session_id": self.session_id})
            if not db_data:
                self.collection.insert_one({
                    "session_id": self.session_id,
                    "messages": []
                })
                db_data = self.collection.find_one({"session_id": self.session_id})

            db_data["_id"] = str(db_data["_id"])
            self.redis_wrapper.setex(self.session_id, 1800, json.dumps(db_data))
            self.memory.chat_memory.messages = messages_from_dict(db_data["messages"])
            logger.info(f"added data : {self.session_id} in redis cache ")

        else:
            cache_data = self.redis_wrapper.get(self.session_id)
            logger.info(f" Found cache data: {self.session_id}")
            self.memory.chat_memory.messages = messages_from_dict(cache_data["messages"])
            logger.warning(f"Conversations loaded into memory  of thread id {self.session_id}")

    def clear(self) -> None:
        """ Abstract method call of BaseChatMessageHistory """
        pass
