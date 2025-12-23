import json
from langchain_core.messages import AIMessage
from loguru import logger
from core.db.queries import store_assistant_response
from common import publish_token, run_async
from common.redis import RedisWrapper
from common.rag.conversation_memory_service import ConversationMemoryStorage
from core.config import settings


class BaseService:
    """ Class for the base service for RAG """

    def result_generation(self, output, thread_id, assistant_message, db_ml_engine, memory, sources):
        """ Generate the result and publish to the redis channel """
        tokens = []
        try:
            redis_wrapper = RedisWrapper(db=settings.REDIS_MESSAGE_STREAMING_DB)
            channel = str(assistant_message.id)
            try:
                for token in output:
                    safe_token = token.replace("\n", "\\n")
                    tokens.append(token)
                    publish_token(safe_token, channel)

                logger.info(f"Result published to redis channel: {str(assistant_message.id)}")
                redis_wrapper.set(f"{channel}:sources", sources, expire=3600 * 4)
                publish_token("__done__", channel)
                result = AIMessage(content=output)
                run_async(
                    ConversationMemoryStorage(thread_id, memory).store_message_db_and_cache(result)
                )
                store_assistant_response(output, assistant_message, db_ml_engine, sources, status=True)

            except Exception as e:
                logger.error(f"Error occurred while generating the markdown result: {e}")
                publish_token("__done__", channel)

                partial_result = ''.join(tokens)
                store_assistant_response(partial_result, assistant_message, db_ml_engine,  sources, status=False)

        except Exception as e:
            logger.error(f"Error occurred while generating the result: {e}")
            store_assistant_response("", assistant_message, db_ml_engine, status=False)
