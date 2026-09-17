from src.client import generate_response
from src.models import LLMResponse
from src.prompts import(
    SUMMARIZER_SYSTEM_PROMPT,
    build_summary_prompt
)


def summarize_text(
        text: str,
        max_sentences: int = 3,
) -> LLMResponse:
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

    if max_sentences <1 :
        raise ValueError("max_sentences must be at least 1.")

    prompt = build_summary_prompt(
        text=text,
        max_sentences=max_sentences
    )

    return generate_response(
        prompt = prompt,
        instructions=SUMMARIZER_SYSTEM_PROMPT,
    )
