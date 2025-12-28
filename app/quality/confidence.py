CONFIDENCE_THRESHOLD = 0.60


def is_confident(results) -> bool:
    """
    Determines if the top result is strong enough to answer.
    """
    if not results:
        return False

    return results[0]["score"] >= CONFIDENCE_THRESHOLD
