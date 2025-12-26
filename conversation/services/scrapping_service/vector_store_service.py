import re
from typing import List
from pymilvus import (
    connections,
    utility,
    Collection,
    FieldSchema,
    CollectionSchema,
    DataType,
)
from langchain.schema import Document
from core.config import embedding
from conversation.services.scrapping_service.hybrid_chunking import HybridChunker
from conversation.services.scrapping_service.sparse_encoder import BM25SparseEncoder


class EmbeddingVectorStore:
    """
    Hybrid Embedding Vector Store
    - Dense embeddings → Milvus HNSW index
    - Sparse embeddings → stored in metadata (BM25)
    """

    def __init__(self):
        connections.connect(host="localhost", port="19530")
        self.chunker = HybridChunker()

    def generate_collection_name(self, country: str, url: str) -> str:
        formatted_country = country.lower().replace(" ", "_")
        safe_url = re.sub(r"[^a-zA-Z0-9_]", "_", url)[:200]
        return f"{formatted_country}_{safe_url}"

    def _prepare_embeddings(self, docs: List[Document]):
        texts = [d.page_content for d in docs]

        dense_vectors = embedding.embed_documents(texts)

        sparse_encoder = BM25SparseEncoder(texts)
        sparse_vectors = [sparse_encoder.encode(t) for t in texts]

        return dense_vectors, sparse_vectors

    def _create_collection(self, name: str, dim: int) -> Collection:
        fields = [
            FieldSchema(
                name="id",
                dtype=DataType.INT64,
                is_primary=True,
                auto_id=True,
            ),
            FieldSchema(
                name="dense_vector",
                dtype=DataType.FLOAT_VECTOR,
                dim=dim,
            ),
            FieldSchema(
                name="text",
                dtype=DataType.VARCHAR,
                max_length=65535,
            ),
            FieldSchema(
                name="metadata",
                dtype=DataType.JSON,
            ),
        ]

        schema = CollectionSchema(
            fields=fields,
            description="Hybrid RAG Collection (Dense indexed, Sparse metadata)",
        )

        collection = Collection(name=name, schema=schema)

        collection.create_index(
            field_name="dense_vector",
            index_params={
                "index_type": "HNSW",
                "metric_type": "COSINE",
                "params": {"M": 16, "efConstruction": 200},
            },
        )

        collection.load()
        return collection

    def embedding_vector_store_service(
        self,
        documents: List[Document],
        country: str,
        main_url: str,
    ):
        if not documents:
            return None, None

        collection_name = self.generate_collection_name(country, main_url)
        chunks = self.chunker.chunk(documents)
        dense_vecs, sparse_vecs = self._prepare_embeddings(chunks)

        if utility.has_collection(collection_name):
            collection = Collection(collection_name)
        else:
            collection = self._create_collection(
                collection_name, dim=len(dense_vecs[0])
            )

        collection.insert(
            [
                dense_vecs,
                [c.page_content for c in chunks],
                [
                    {
                        **c.metadata,
                        "sparse_vector": sparse_vecs[i],
                    }
                    for i, c in enumerate(chunks)
                ],
            ]
        )
        collection.flush()
        collection.load()
        return collection, collection_name
