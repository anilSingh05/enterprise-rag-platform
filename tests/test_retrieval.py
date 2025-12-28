import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.prompt.prompt_builder import build_prompt
from app.retrieval import context_selector
from app.retrieval.retriever import Retriever
from app.ingestion.ingest_fintech_docs import ingest
from app.quality.confidence import is_confident

vector_store = ingest()
retriever = Retriever(vector_store)

query = "What are the KYC requirements for customers?"
results = retriever.retrieve(query)

for r in results:
    print(r["score"], r["metadata"]["source"])

if is_confident(results):
    print("Answer Allowed")
else:
    print("Refuse to Answer")
    
context = context_selector.select(results)

system_prompt, user_prompt = build_prompt(context, query)

###. answer = call_llm(system_prompt, user_prompt)