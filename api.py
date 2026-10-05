from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from src.qa import answer_question
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

class AskRequest(BaseModel):
    context: str = Field(min_length=1)
    question: str = Field(min_length=1)


class AskResponse(BaseModel):
    answer: str
    usage: TokenUsageResponse

@app.get("/health")
def health_check():
    """Return API health status."""

    return {"status": "ok"}


@app.post("/summarize", response_model=SummarizeResponse)
def summarize(request: SummarizeRequest):
    """Summarize the provided text."""

    try:
        response = summarize_text(
            text=request.text,
            max_sentences=request.max_sentences,
        )
    except RuntimeError as error:
        raise HTTPException(
            status_code=502,
            detail=str(error),
        ) from error

    return SummarizeResponse(
        summary=response.text,
        usage=TokenUsageResponse(
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
            total_tokens=response.usage.total_tokens,
        ),
    )

@app.post("/ask", response_model=AskResponse)
def ask_question(request: AskRequest):
    """Answer a question using the provided context."""

    try:
        response = answer_question(
            context=request.context,
            question=request.question,
        )
    except RuntimeError as error:
        raise HTTPException(
            status_code=502,
            detail=str(error),
        ) from error

    return AskResponse(
        answer=response.text,
        usage=TokenUsageResponse(
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
            total_tokens=response.usage.total_tokens,
        ),
    )

