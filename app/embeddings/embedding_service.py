from openai import OpenAI
import numpy as np
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def create_embedding(text: str) -> np.ndarray:
    """
    Creates a vector embedding for input text.
    Used both during ingestion (documents) and runtime (queries).
    """

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )

    return np.array(response.data[0].embedding, dtype="float32")
