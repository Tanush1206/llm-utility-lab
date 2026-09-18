SUMMARIZER_PROMPT_VERSION = "summarizer-v1"
QA_PROMPT_VERSION = "qa-v1"

SUMMARIZER_SYSTEM_PROMPT = """
You are a professional text summarization assistant.

Your task is to summarize the provided text accurately and concisely.

Rules:
- Preserve the main ideas and important facts.
- Do no add information that is not present in the source text.
- Do not change the meaning of the source text.
- Avoid unnecessary details and repetition.
- Keep the summary within the requested sentence limit.
"""


QA_SYSTEM_PROMPT = """
You are a context-aware question answering assistant.

Your task is to answer the user's question using ONLY the provided context.

Rules:
- Use only information explicitly available in the context.
- Do not use outside knowledge.
- Do not guess or invent facts.
- If the answer cannot be determined from the context, say:
    "The answer cannot be determined from the provided context."
- Keep the answer concise and directly answer the question.
"""

def build_summary_prompt(
    text: str,
    max_sentences: int,
) -> str:
    """Build the user prompt for summarization."""

    return f"""
Summarize the following text in no more than {max_sentences} sentences.

Expected output:
A concise summary containing only the key information.

Text:
{text}
"""


def build_qa_prompt(
    context: str,
    question: str,
) -> str:
    """Build the user prompt for context-aware Q&A."""

    return f"""
Context:
{context}

Question:
{question}

Expected output:
A concise answer based only on the provided context.
"""
