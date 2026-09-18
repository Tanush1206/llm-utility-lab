from src.client import generate_response
from src.models import LLMResponse
from src.prompts import(
    QA_SYSTEM_PROMPT,
    build_qa_prompt
)

def answer_question(
        context: str,
        question: str,
) -> LLMResponse:
    """
    Answer a question using only the provided context.

    Args:
    context: Source information that the model should use.
    question: User's question.

    Returns:
    An answer grounded in the provided context.
    """

    if not context.strip():
        raise ValueError("Context cannot be empty.")

    if not question.strip():
        raise ValueError("Question cannot be empty.")

    prompt = build_qa_prompt(
        context=context,
        question=question,
    )

    return generate_response(
        prompt=prompt,
        instructions=QA_SYSTEM_PROMPT,
        temperature=0.1
    )
