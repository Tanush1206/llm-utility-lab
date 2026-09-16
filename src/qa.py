from src.client import generate_response

SYSTEM_PROMPT = """
You area context-aware question answering assistant.

Answer the user's question using ONLY the provided content.

Rules:
- Do not use information that is not present in the context.
- Do not make up facts or details.
- If the answer cannot be found in the context, clearly say:
    "The answer cannot be determined from the provided context."
- Keep the answer concise and directly answer the question.
"""


def answer_question(
        context: str,
        question: str,
) -> str:
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

    prompt = f"""

{SYSTEM_PROMPT}

Context:
{context}

Question:
{question}

Answer:
"""

    return generate_response(prompt)
