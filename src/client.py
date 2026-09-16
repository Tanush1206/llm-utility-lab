import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

def get_llm_client() -> OpenAI:
    """Create and return an OpenAI API client."""
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is not set."
            "Add it to your .env file."
        )

    return OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1"
    )

def generate_response(
        prompt: str,
        model: str = "openai/gpt-oss-20b",
) -> str:
    """Generate a text response using the OpenAI Response API."""
    client = get_llm_client()

    response = client.responses.create(
        model=model,
        input=prompt
    )

    return response.output_text
