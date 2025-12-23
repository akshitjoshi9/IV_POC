import re
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_milvus import Milvus
from pymilvus import connections, utility
from core.config import embedding


class EmbeddingVectorStore:
    """ This class contains service for embedding model and vector DB creation """
    def __init__(self):
        connections.connect(
            host="localhost",
            port="19530"
        )

    def generate_collection_name(self, country, url):
        formatted_country = country.lower().replace(" ", "_")
        safe_url = re.sub(r"[^a-zA-Z0-9_]", "_", url)
        safe_url = safe_url[:200]
        collection_name = f"{formatted_country}_{safe_url}"
        return collection_name

    def embedding_service(self, documents):
        """This service uses a text splitter to chunk documents"""
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        docs = text_splitter.split_documents(documents)
        return docs

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