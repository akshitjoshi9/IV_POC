from langchain_core.messages import HumanMessage

from common.rag.conversation_memory_service import ConversationMemoryStorage
from common.rag.rag_service import RagAgentService
from common.response import error_response
from langchain.memory import ConversationBufferMemory
from common import run_async
from core.db.queries.message import get_country, get_category


class MainService:

    def main_executor(self, body, user_message, assistant_message, db_ml_engine):
        """ This service communicate with API and RAG service call from here"""

        thread_id = str(body.thread_id)
        country_id = str(body.country_id)
        sub_category_id = str(body.sub_category_id)
        memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True, output_key="answer"
        )
        ConversationMemoryStorage(thread_id, memory)
        query = HumanMessage(content=user_message.content)
        run_async(
            ConversationMemoryStorage(thread_id, memory).store_message_db_and_cache(query)
        )
        country = get_country(country_id, db_ml_engine)
        category = get_category(sub_category_id, db_ml_engine)
        if not country:
            return error_response(status_code=404, message="Country not found")

        return RagAgentService(country.name, category.name, query).execute(
            thread_id, assistant_message, memory, db_ml_engine
        )
