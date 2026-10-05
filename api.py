import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from src.qa import answer_question
from src.summarizer import summarize_text

app = FastAPI(
    title="LLM Utility Lab API",
    description=(
        "Production-oriented API for text summarization and "
        "context-aware question answering."
    ),
    version="1.0.0",
)

logger = logging.getLogger("llm_utility_lab.api")


@app.exception_handler(RuntimeError)
async def runtime_error_handler(request: Request, error: RuntimeError):
    logger.error(
        "LLM API error | method=%s | path=%s | error_type=%s",
        request.method,
        request.url.path,
        type(error).__name__,
    )

    return JSONResponse(
        status_code=502,
        content={"detail": str(error)},
    )


@app.exception_handler(Exception)
async def unexpected_error_handler(request: Request, error: Exception):
    logger.exception(
        "Unexpected API error | method=%s | path=%s",
        request.method,
        request.url.path,
    )

    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error."},
    )

class SummarizeRequest(BaseModel):
    text: str = Field(min_length=1)
    max_sentences: int = Field(default=3, ge=1)

    model_config = {
        "json_schema_extra": {
            "example": {
                "text": (
                    "The company was founded in 2018 and develops "
                    "cloud-based accounting software."
                ),
                "max_sentences": 1,
            }
        }
    }


class TokenUsageResponse(BaseModel):
    input_tokens: int
    output_tokens: int
    total_tokens: int


class SummarizeResponse(BaseModel):
    summary: str
    usage: TokenUsageResponse


class AskRequest(BaseModel):
    context: str = Field(min_length=1)
    question: str = Field(min_length=1)

    model_config = {
        "json_schema_extra": {
            "example": {
                "context": "The company was founded in 2018.",
                "question": "When was the company founded?",
            }
        }
    }


class AskResponse(BaseModel):
    answer: str
    usage: TokenUsageResponse


@app.get(
    "/health",
    tags=["Health"],
    summary="Check API health",
)
def health_check():
    """Return API health status."""

    return {"status": "ok"}


@app.post(
    "/summarize",
    response_model=SummarizeResponse,
    tags=["LLM"],
    summary="Summarize text",
)
def summarize(request: SummarizeRequest):
    """Summarize the provided text."""

    response = summarize_text(
        text=request.text,
        max_sentences=request.max_sentences,
    )

    return SummarizeResponse(
        summary=response.text,
        usage=TokenUsageResponse(
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
            total_tokens=response.usage.total_tokens,
        ),
    )


@app.post(
    "/ask",
    response_model=AskResponse,
    tags=["LLM"],
    summary="Answer a question from context",
)
def ask_question(request: AskRequest):
    """Answer a question using the provided context."""

    response = answer_question(
        context=request.context,
        question=request.question,
    )

    return AskResponse(
        answer=response.text,
        usage=TokenUsageResponse(
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
            total_tokens=response.usage.total_tokens,
        ),
    )
