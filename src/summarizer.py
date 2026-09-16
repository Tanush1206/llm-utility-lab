from src.client import generate_response

SYSTEM_PROMPT = """
You are a professional text summarization assistant.

Summarize the provided text accurately and concisely.
Preserve the key facts, important details, and main ideas.
Do not add information that is not present in the source text
"""

def summarize_text(
        text: str,
        max_sentences: int = 3,
) -> str:
    """
    Summarize the given text using an LLM.

    Args:
        text: The source text to summarize.
        max_sentences: Maximum number of sentences in the summary.

    Returns:
        A concise summary of the input text.
    """

    if not text.strip():
        raise ValueError("Text to summarize cannot be empty.")

    prompt=f"""
{SYSTEM_PROMPT}

Return a summary of no more than {max_sentences} sentences.

Text to summarize:
{text}
"""

    return generate_response(prompt)
