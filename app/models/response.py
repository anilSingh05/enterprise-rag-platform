from pydantic import BaseModel
from typing import List, Optional


class AskResponse(BaseModel):
    answer: Optional[str]
    confidence: float
    sources: List[str]
    refused: bool

