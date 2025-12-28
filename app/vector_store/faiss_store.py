import faiss
import numpy as np
from typing import List, Dict


class FaissVectorStore:
    """
    Thin abstraction over FAISS.
    Keeps vectors + metadata aligned by index position.
    """

    def __init__(self, embedding_dim: int):
        self.index = faiss.IndexFlatIP(embedding_dim)  # cosine similarity
        self.metadata: List[Dict] = []

    def add(self, embedding: np.ndarray, metadata: Dict):
        faiss.normalize_L2(embedding.reshape(1, -1))
        self.index.add(embedding.reshape(1, -1))
        self.metadata.append(metadata)

    def search(self, query_embedding: np.ndarray, top_k: int = 5):
        faiss.normalize_L2(query_embedding.reshape(1, -1))
        scores, indices = self.index.search(query_embedding.reshape(1, -1), top_k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue
            results.append({
                "score": float(score),
                "metadata": self.metadata[idx]
            })
        return results
# Example usage:
# store = FaissVectorStore(embedding_dim=1536)
# store.add(embedding_vector, {"source": "doc1", "page": 1})
# results = store.search(query_vector, top_k=3)