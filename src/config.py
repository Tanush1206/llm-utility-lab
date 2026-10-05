import os

from dotenv import load_dotenv

load_dotenv()

DEFAULT_GROQ_MODEL = "openai/gpt-oss-20b"
DEFAULT_GROQ_TEMPERATURE = 0.1

def get_groq_api_key() -> str:
    """Return the configured Groq API key."""

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key or not api_key.strip():
        raise ValueError(
            "GROQ_API_KEY is not set. Add it to your .env file."
        )

    return api_key.strip()

def get_groq_model() -> str:
    """Return the configured Groq model."""

    model = os.getenv(
        "GROQ_MODEL",
        DEFAULT_GROQ_MODEL
    )

    if not model.strip():
        raise ValueError(
            "GROQ_MODEL cannot be empty."
        )

    return model.strip()

def get_groq_temperature() -> str:
    """Return the configured Groq temperature."""

    raw_temperature = os.getenv(
        "GROQ_TEMPERATURE",
        DEFAULT_GROQ_TEMPERATURE
    )

    try:
        temperature = float(raw_temperature)
    except ValueError as error:
        raise ValueError(
            "GROQ_TEMPERATURE must be a valid number."
        ) from error

    if not 0 <= temperature <= 2:
        raise ValueError(
            "GROQ_TEMPERATURE must be between 0 and 2."
        )

    return temperature
