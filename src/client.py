from openai import APIConnectionError, APIStatusError, OpenAI

from src.config import (
    get_groq_api_key,
    get_groq_model,
    get_groq_temperature,
    get_groq_timeout,
)
from src.models import LLMResponse, TokenUsage
from time import perf_counter
from src.logging_config import get_logger

logger = get_logger("client")

def get_default_model() -> str:
    """Return the configured default LLM model."""

    return get_groq_model()


def get_default_temperature() -> float:
    """Return the configured default temperature."""

    return get_groq_temperature()


def get_llm_client() -> OpenAI:
    """Create and return an OpenAI-compatible Groq client."""

    api_key = get_groq_api_key()
    timeout = get_groq_timeout()

    return OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1",
        timeout=timeout,
    )


def generate_response(
    prompt: str,
    instructions: str = "",
    model: str | None = None,
    temperature: float | None = None,
) -> LLMResponse:
    """Generate a text response using the Groq Response API."""

    if not prompt.strip():
        raise ValueError("Prompt cannot be empty.")

    start_time = perf_counter()

    logger.info(
        "LLM request started | model=%s",
        model or get_default_model(),
    )

    client = get_llm_client()

    try:
        request_args = {
            "model": model or get_default_model(),
            "input": prompt,
        }

        configured_temperature = (
            temperature
            if temperature is not None
            else get_default_temperature()
        )

        request_args["temperature"] = configured_temperature

        if instructions.strip():
            request_args["instructions"] = instructions

        response = client.responses.create(**request_args)

        output = response.output_text

        if not output or not output.strip():
            raise RuntimeError("The LLM returned an empty response.")

        usage = TokenUsage(
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
            total_tokens=response.usage.total_tokens,
        )

        duration = perf_counter() - start_time

        logger.info(
            "LLM request completed | model=%s | duration=%.2fs | "
            "input_tokens=%d | output_tokens=%d | total_tokens=%d",
            model or get_default_model(),
            duration,
            usage.input_tokens,
            usage.output_tokens,
            usage.total_tokens,
        )

        return LLMResponse(
            text=output.strip(),
            usage=usage,
        )

    except APIStatusError as error:
        logger.error(
            "LLM request failed | status_code=%s | error_type=%s",
            error.status_code,
            type(error).__name__,
        )

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
        logger.error(
            "LLM request failed | error_type=%s",
            type(error).__name__,
        )

        raise RuntimeError(
            "Could not connect to Groq. Check your internet connection."
        ) from error
