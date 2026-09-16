import os

from dotenv import load_dotenv
from openai import OpenAI, APIConnectionError, APIStatusError

load_dotenv()

def get_llm_client() -> OpenAI:
    """Create and return an OpenAI-compatible Groq client."""
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
    """Generate a text response using the Groq Response API."""

    if not prompt.strip():
        raise ValueError("Prompt cannot be empty.")

    client = get_llm_client()

    try:
        response = client.responses.create(
            model=model,
            input= prompt,
        )

        output = response.output_text

        if not output or not output.strip():
            raise RuntimeError("The LLM returned an empty response.")

        return output.strip()

    except APIStatusError as error:
        status_code = error.status_code

        if status_code == 401:
            raise RuntimeError(
                "Authentication failed. Check your GROQ_API_KEY."
            ) from error
        if status_code == 429:
            raise RuntimeError(
                "Groq rate limit reached. Please try again later."
            ) from error
        if status_code >= 500:
            raise RuntimeError(
                "Groq server error. Please try again later."
            ) from error
        raise RuntimeError(
            f"Groq API request failed with status: {status_code}."
        ) from error

    except APIConnectionError as error:
        raise RuntimeError(
            "Could not connect to Groq. Check you internet connection."
        )from error
