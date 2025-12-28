from app.embeddings.embedding_service import create_embedding
from app.vector_store.faiss_store import FaissVectorStore


class Retriever:
    """
    Handles query embedding and vector retrieval.
    """

    def __init__(self, vector_store: FaissVectorStore):
        self.vector_store = vector_store

    def retrieve(self, query: str, top_k: int = 5):
        """
        Embeds query and retrieves top-k similar chunks.
        """
        query_embedding = create_embedding(query)
        return self.vector_store.search(query_embedding, top_k=top_k)
# Example usage:
# retriever = Retriever(vector_store)
# results = retriever.retrieve("What is fintech?", top_k=3)
