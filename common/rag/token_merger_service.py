from pydantic import BaseModel, Field
from typing import Dict, List, ClassVar
from common.constant import QUESTION_WISE_RULES
from langchain.schema import Document
from langchain_core.retrievers import BaseRetriever
from rank_bm25 import BM25Okapi


class PromptConfig(BaseModel):
    question_rules: Dict[str, dict] = Field(default_factory=lambda: QUESTION_WISE_RULES)

    def get_rule(self, query: str) -> dict:
        qnorm = query.lower()
        for k, rule in self.question_rules.items():
            if k.lower() in qnorm:
                return rule
        return {}


class TopKMergerRetriever(BaseRetriever):
    retrievers: List[BaseRetriever] = Field(...)
    k: int = Field(default=30)
    canonical_question: str | None = None
    config: ClassVar[PromptConfig] = PromptConfig()

    def _rerank_bm25(self, query, docs):
        tokenized_corpus = [doc.page_content.lower().split() for doc in docs]
        bm25 = BM25Okapi(tokenized_corpus)
        tokenized_query = query.lower().split()
        scores = bm25.get_scores(tokenized_query)
        for doc, score in zip(docs, scores):
            doc.metadata["score"] = float(score)
        docs_sorted = sorted(docs, key=lambda d: d.metadata["score"], reverse=True)
        return docs_sorted

    def _apply_preference_rules(self, query: str, docs: List[Document]) -> List[Document]:
        """Boost scores of preferred sources instead of filtering."""
        lookup_query = self.canonical_question
        rules = self.config.get_rule(lookup_query)
        if rules:
            keywords = rules.get("preferred_source_contains", [])
            prioritized = [
                d for d in docs
                if all(k.lower() in d.metadata.get("source", "").lower() for k in keywords)
            ]
            return prioritized if prioritized else docs
        else:
            return self._rerank_bm25(query, docs)

    def _get_relevant_documents(self, query: str) -> List[Document]:
        all_docs = []
        for r in self.retrievers:
            docs = r.get_relevant_documents(query)
            all_docs.extend(docs)

        all_docs = self._apply_preference_rules(query, all_docs)
        return all_docs[:self.k]

    async def _aget_relevant_documents(self, query: str) -> List[Document]:
        return self._get_relevant_documents(query)