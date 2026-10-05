from fastapi.testclient import TestClient

from api import app
from src.models import LLMResponse, TokenUsage


client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_summarize_endpoint(monkeypatch):
    fake_response = LLMResponse(
        text="Founded in 2018.",
        usage=TokenUsage(
            input_tokens=10,
            output_tokens=5,
            total_tokens=15,
        ),
    )

    monkeypatch.setattr(
        "api.summarize_text",
        lambda text, max_sentences: fake_response,
    )

    response = client.post(
        "/summarize",
        json={
            "text": "The company was founded in 2018.",
            "max_sentences": 1,
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "summary": "Founded in 2018.",
        "usage": {
            "input_tokens": 10,
            "output_tokens": 5,
            "total_tokens": 15,
        },
    }


def test_summarize_rejects_empty_text():
    response = client.post(
        "/summarize",
        json={
            "text": "",
            "max_sentences": 1,
        },
    )

    assert response.status_code == 422


def test_summarize_rejects_invalid_max_sentences():
    response = client.post(
        "/summarize",
        json={
            "text": "Some text.",
            "max_sentences": 0,
        },
    )

    assert response.status_code == 422

def test_ask_endpoint(monkeypatch):
    fake_response = LLMResponse(
        text="2018",
        usage=TokenUsage(
            input_tokens=10,
            output_tokens=5,
            total_tokens=15,
        ),
    )

    monkeypatch.setattr(
        "api.answer_question",
        lambda context, question: fake_response,
    )

    response = client.post(
        "/ask",
        json={
            "context": "The company was founded in 2018.",
            "question": "When was the company founded?",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "answer": "2018",
        "usage": {
            "input_tokens": 10,
            "output_tokens": 5,
            "total_tokens": 15,
        },
    }


def test_ask_rejects_empty_context():
    response = client.post(
        "/ask",
        json={
            "context": "",
            "question": "When was the company founded?",
        },
    )

    assert response.status_code == 422

def test_summarize_handles_llm_error(monkeypatch):
    def raise_error(text, max_sentences):
        raise RuntimeError("Groq rate limit reached. Please try again later.")

    monkeypatch.setattr("api.summarize_text", raise_error)

    response = client.post(
        "/summarize",
        json={
            "text": "The company was founded in 2018.",
            "max_sentences": 1,
        },
    )

    assert response.status_code == 502
    assert response.json() == {
        "detail": "Groq rate limit reached. Please try again later."
    }


def test_ask_handles_llm_error(monkeypatch):
    def raise_error(context, question):
        raise RuntimeError("Groq server error. Please try again later.")

    monkeypatch.setattr("api.answer_question", raise_error)

    response = client.post(
        "/ask",
        json={
            "context": "The company was founded in 2018.",
            "question": "When was the company founded?",
        },
    )

    assert response.status_code == 502
    assert response.json() == {
        "detail": "Groq server error. Please try again later."
    }
