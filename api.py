from fastapi import FastAPI
from pydantic import BaseModel, Field

from src.summarizer import summarize_text


app = FastAPI(
    title="LLM Utility Lab API",
    version="1.0.0",
)


class SummarizeRequest(BaseModel):
    text: str = Field(min_length=1)
    max_sentences: int = Field(default=3, ge=1)


class TokenUsageResponse(BaseModel):
    input_tokens: int
    output_tokens: int
    total_tokens: int


class SummarizeResponse(BaseModel):
    summary: str
    usage: TokenUsageResponse


@app.get("/health")
def health_check():
    """Return API health status."""

    return {"status": "ok"}


@app.post("/summarize", response_model=SummarizeResponse)
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
