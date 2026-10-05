from fastapi import FastAPI


app = FastAPI(
    title="LLM Utility Lab API",
    version="1.0.0",
)


@app.get("/health")
def health_check():
    """Return API health status."""

    return {"status": "ok"}
