import re
from langchain_milvus import Milvus
from pymilvus import connections, utility
from core.config import embedding
from conversation.services.scrapping_service.hybrid_chunking import HybridChunker


class EmbeddingVectorStore:
    """ This class contains service for embedding model and vector DB creation """
    def __init__(self):
        connections.connect(
            host="localhost",
            port="19530"
        )
        self.chunker = HybridChunker()

    def generate_collection_name(self, country, url):
        formatted_country = country.lower().replace(" ", "_")
        safe_url = re.sub(r"[^a-zA-Z0-9_]", "_", url)
        safe_url = safe_url[:200]
        collection_name = f"{formatted_country}_{safe_url}"
        return collection_name

    def embedding_service(self, documents):
        """This service uses a text splitter to chunk documents"""
        if not documents:
            return []

        chunks = self.chunker.chunk(documents)
        return chunks

    def vector_store_service(self, docs, collection_name):
        """Store vector data into Milvus vector DB"""
        if utility.has_collection(collection_name):
            vectorstore = Milvus(
                embedding_function=embedding,
                collection_name=collection_name,
                auto_id=True
            )
            vectorstore.add_documents(docs)
            return vectorstore
        else:
            return Milvus.from_documents(
                documents=docs,
                embedding=embedding,
                collection_name=collection_name,
                auto_id=True
            )

    def embedding_vector_store_service(self, documents, country, main_url):
        """Convert and store documents into vector DB"""
        collection_name = self.generate_collection_name(country, main_url)
        docs = self.embedding_service(documents)
        vectorstore = self.vector_store_service(docs, collection_name)
        return vectorstore, collection_name