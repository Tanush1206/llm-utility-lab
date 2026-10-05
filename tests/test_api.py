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
