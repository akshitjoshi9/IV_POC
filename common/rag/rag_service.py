import json
from langchain.chains import ConversationalRetrievalChain
from langchain_community.vectorstores import Milvus
from pymilvus import connections, utility, Collection

from common.rag import BaseService
from common.rag.prompt import get_custom_react_task
from common.rag.token_merger_service import TopKMergerRetriever
from core.config import llm, embedding, settings


class RagAgentService:

    def __init__(self, country, category, query):
        self.country = country
        self.query = query
        self.category = category
        connections.connect("default", host=settings.MILVUS_HOST, port=settings.MILVUS_PORT)
        self.reasoning_instructions = (
            f"You are an expert in {self.country} medicines regulation. "
            f"Use only information returned by the tools. "
            f"When a law mentions a generic authority, determine the concrete organisation in the "
            f"{self.country} context and name it explicitly."
        )
        self.prompt = get_custom_react_task(self.reasoning_instructions, self.query.content, self.category)
        self.retriever = self._build_retriever_for_country(self.country)


    @staticmethod
    def dynamic_k_count(chunk_count, max_top_k=100, max_fetch_k=50):
        top_k = min(max(chunk_count // 5, 20), max_top_k)
        fetch_k = min(max(top_k // 2, 5), max_fetch_k)
        return top_k, fetch_k

    def _build_retriever_for_country(self, country: str):
        all_collections = utility.list_collections()
        country_prefix = f"{country.lower().replace(' ', '_')}_"
        country_collections = [c for c in all_collections if c.startswith(country_prefix)]

        retrievers = []
        for col_name in country_collections:
            collection = Collection(col_name)
            collection.load()
            vectordb = Milvus(
                embedding_function=embedding,
                collection_name=col_name,
            )
            total_chunks = collection.num_entities
            top_k, fetch_k = self.dynamic_k_count(total_chunks)

            retrievers.append(
                vectordb.as_retriever(
                    search_type="mmr",
                    search_kwargs={
                        "k": fetch_k,
                        "fetch_k": top_k,
                        "param": {"ef": top_k + 30},
                    },
                )
            )
        return TopKMergerRetriever(retrievers=retrievers, k=30, canonical_question=self.query.content)

    def format_docs(self, docs):
        formatted = []
        for d in docs:
            source = d.metadata.get("source", "")
            formatted.append(f"Content:\n{d.page_content}\nSource: {source}")
        return "\n\n".join(formatted)

    def execute(self, thread_id, assistant_message, memory, db_ml_engine):
        qa_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=self.retriever,
            chain_type="stuff",
            return_source_documents=True,
            memory=memory,
            combine_docs_chain_kwargs={"prompt": self.prompt},
            output_key="answer"
        )

        out = qa_chain.invoke({"question": self.query.content})
        context = self.format_docs(out.get("source_documents", []))

        answer_with_sources = llm.invoke(
            self.prompt.format_messages(
                chat_history=memory.chat_memory.messages,
                question=self.query.content,
                context=context
            )
        )
        answer_text = answer_with_sources.content.strip()

        parsed = None
        try:
            parsed = json.loads(answer_text)
        except json.JSONDecodeError:
            import re
            match = re.search(r"\{.*\}", answer_text, re.DOTALL)
            if match:
                try:
                    parsed = json.loads(match.group())
                except json.JSONDecodeError:
                    pass

        if not parsed:
            parsed = {"final_answer": answer_text, "source": []}

        answer_text = parsed.get("final_answer", answer_text)
        sources = parsed.get("source", [])

        final_sources = []
        for source in sources:
            suffix = "data.xht?view=snippet&wrap=true"
            if source.endswith(suffix):
                final_sources.append(source.replace("/" + suffix, ""))
            else:
                final_sources.append(source)

        BaseService().result_generation(
            output=answer_text,
            thread_id=thread_id,
            assistant_message=assistant_message,
            db_ml_engine=db_ml_engine,
            memory=memory,
            sources=final_sources
        )
