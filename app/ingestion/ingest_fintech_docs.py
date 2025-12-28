import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from vector_store.faiss_store import FaissVectorStore
from embeddings.embedding_service import create_embedding
from ingestion.chuncking import TextChunker


DATA_DIR = "data/fintech"


def ingest():
    chunker = TextChunker()
    vector_store = None
##  Loop through all text files in the data directory
    for filename in os.listdir(DATA_DIR):
        if not filename.endswith(".txt"):
            continue
##  Read file content
        filepath = os.path.join(DATA_DIR, filename)
        text = open(filepath).read()
##  Chunk text
        chunks = chunker.chunk_text(text)
##  Create embeddings and add to vector store
        for chunk in chunks:
            embedding = create_embedding(chunk.text)
##  Initialize vector store if not already done
            if vector_store is None:
                vector_store = FaissVectorStore(len(embedding))
##  Add to vector store with metadata
            vector_store.add(
                embedding=embedding,
                metadata={
                    "source": filename,
                    "domain": "fintech",
                    "version": "v1",
                    "text": chunk.text
                }
            )
##  Final log
    print(f"Ingestion complete. Total vectors: {vector_store.index.ntotal}")
    return vector_store


if __name__ == "__main__":
    ingest()
