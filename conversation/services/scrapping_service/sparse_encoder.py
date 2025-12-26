from rank_bm25 import BM25Okapi
from typing import List, Dict


class BM25SparseEncoder:
    def __init__(self, corpus_texts: List[str]):
        self.tokenized_corpus = [doc.lower().split() for doc in corpus_texts]
        self.bm25 = BM25Okapi(self.tokenized_corpus)

    def encode(self, text: str) -> Dict[int, float]:
        tokens = text.lower().split()
        scores = self.bm25.get_scores(tokens)

        sparse_vector = {
            idx: float(score)
            for idx, score in enumerate(scores)
            if score > 0
        }
        return sparse_vector
