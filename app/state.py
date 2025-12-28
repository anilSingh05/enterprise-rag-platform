from app.ingestion.ingest_fintech_docs import ingest

vector_store = None


def get_vector_store():
    global vector_store
    if vector_store is None:
        vector_store = ingest()
    return vector_store
