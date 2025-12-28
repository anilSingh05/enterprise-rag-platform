from fastapi import APIRouter
from fastapi import Request
from app.retrieval.retriever import Retriever
from app.retrieval.context_selector import ContextSelector
from app.quality.confidence import is_confident
from app.prompt.prompt_builder import build_prompt
from app.llm.client import generate_answer
from app.models.response import AskResponse

router = APIRouter()


@router.post("/ai/ask", response_model=AskResponse)
def ask_question(request: Request, question: str):
    """
    End-to-end RAG pipeline exposed via API.
    """

    vector_store = request.app.state.vector_store

    retriever = Retriever(vector_store)
    results = retriever.retrieve(question)
    
    print("Top score:", results[0]["score"])


    if not is_confident(results):
        return AskResponse(
            answer=None,
            confidence=0.0,
            sources=[],
            refused=True
        )

    context_selector = ContextSelector()
    context = context_selector.select(results)

    system_prompt, user_prompt = build_prompt(context, question)
    answer = generate_answer(system_prompt, user_prompt)

    sources = list(
        {r["metadata"]["source"] for r in results}
    )

    return AskResponse(
        answer=answer,
        confidence=results[0]["score"],
        sources=sources,
        refused=False
    )
# Example usage:
# response = ask_question("What are the KYC requirements for customers?")
# print(response.answer)