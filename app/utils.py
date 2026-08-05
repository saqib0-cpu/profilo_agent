def clamp_text(text: str, max_len: int = 4000) -> str:
    """Prevents runaway-long messages from bloating context."""
    if len(text) > max_len:
        return text[:max_len] + "..."
    return text