from fastapi import FastAPI
from app.api.ask import router as ask_router
from app.ingestion.ingest_fintech_docs import ingest


app = FastAPI(title="Enterprise RAG Platform")

app.include_router(ask_router)

@app.on_event("startup")
def startup_event():
    """
    Ingest documents and prepare vector store at startup.
    """
    app.state.vector_store = ingest()

# Example usage:
# uvicorn app.main:app --reload