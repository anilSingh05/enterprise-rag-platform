import tiktoken
from typing import List


class TextChunk:
    """
    Represents a single chunk of text along with token metadata.
    """
    def __init__(self, text: str, tokens: int):
        self.text = text
        self.tokens = tokens


class TextChunker:
    """
    Deterministic chunker.
    This does NOT use an LLM.
    It only splits text based on token limits.
    """

    def __init__(self, model_name: str = "gpt-4o-mini"):
        # Tokenizer only — no API calls
        self.encoder = tiktoken.encoding_for_model(model_name)

    def chunk_text(
        self,
        text: str,
        chunk_size: int = 300,
        overlap: int = 50
    ) -> List[TextChunk]:
        """
        Splits input text into overlapping chunks.

        Why overlap?
        - Prevents loss of meaning across boundaries
        - Improves retrieval quality
        """

        tokens = self.encoder.encode(text)
        chunks = []

        start = 0
        while start < len(tokens):
            end = start + chunk_size
            chunk_tokens = tokens[start:end]

            chunk_text = self.encoder.decode(chunk_tokens)
            chunks.append(TextChunk(chunk_text, len(chunk_tokens)))

            # Move window forward with overlap
            start += chunk_size - overlap

        return chunks
# Example usage:
# chunker = TextChunker()
# chunks = chunker.chunk_text("Your long text here...", chunk_size=300, overlap