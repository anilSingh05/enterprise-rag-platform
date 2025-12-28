import tiktoken

MAX_CONTEXT_TOKENS = 1500


class ContextSelector:
    """
    Selects the most relevant chunks that fit within a token budget.
    """

    def __init__(self, model_name: str = "gpt-4o-mini"):
        self.encoder = tiktoken.encoding_for_model(model_name)

    def select(self, retrieved_chunks):
        """
        Select chunks until token budget is exhausted.
        """
        selected = []
        used_tokens = 0

        for item in retrieved_chunks:
            text = item["metadata"]["text"]
            tokens = len(self.encoder.encode(text))

            if used_tokens + tokens > MAX_CONTEXT_TOKENS:
                break

            selected.append(text)
            used_tokens += tokens

        return selected
# Example usage:
# selector = ContextSelector()
# context = selector.select(retrieved_chunks)   