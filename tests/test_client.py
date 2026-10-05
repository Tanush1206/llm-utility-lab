import pytest
from openai import APIConnectionError, APIStatusError

from src.client import generate_response
from src.models import TokenUsage


class FakeUsage:
    input_tokens = 10
    output_tokens = 5
    total_tokens = 15


class FakeResponse:
    output_text = "2018"
    usage = FakeUsage()


class FakeResponses:
    def create(self, **kwargs):
        return FakeResponse()


class FakeClient:
    def __init__(self):
        self.responses = FakeResponses()


def test_generate_response_returns_llm_response(monkeypatch):
    monkeypatch.setattr(
        "src.client.get_llm_client",
        lambda: FakeClient(),
    )

    response = generate_response(prompt="When was the company founded?")

    assert response.text == "2018"
    assert response.usage.input_tokens == 10
    assert response.usage.output_tokens == 5
    assert response.usage.total_tokens == 15


def test_generate_response_rejects_empty_prompt():
    with pytest.raises(ValueError, match="Prompt cannot be empty"):
        generate_response(prompt="   ")


def test_generate_response_handles_authentication_error(monkeypatch):
    class FakeResponses:
        def create(self, **kwargs):
            raise APIStatusError(
                "Authentication failed",
                response=type(
                    "Response",
                    (),
                    {
                        "status_code": 401,
                        "request": None,
                        "headers": {},
                    },
                )(),
                body=None,
            )

    class FakeClient:
        responses = FakeResponses()

    monkeypatch.setattr(
        "src.client.get_llm_client",
        lambda: FakeClient(),
    )

    with pytest.raises(
        RuntimeError,
        match="Authentication failed",
    ):
        generate_response(prompt="Test")


def test_generate_response_handles_rate_limit_error(monkeypatch):
    class FakeResponses:
        def create(self, **kwargs):
            raise APIStatusError(
                "Rate limit reached",
                response=type(
                    "Response",
                    (),
                    {
                        "status_code": 429,
                        "request": None,
                        "headers": {},
                    },
                )(),
                body=None,
            )

    class FakeClient:
        responses = FakeResponses()

    monkeypatch.setattr(
        "src.client.get_llm_client",
        lambda: FakeClient(),
    )

    with pytest.raises(
        RuntimeError,
        match="Groq rate limit reached",
    ):
        generate_response(prompt="Test")


def test_generate_response_handles_server_error(monkeypatch):
    class FakeResponses:
        def create(self, **kwargs):
            raise APIStatusError(
                "Server error",
                response=type(
                    "Response",
                    (),
                    {
                        "status_code": 500,
                        "request": None,
                        "headers": {},
                    },
                )(),
                body=None,
            )

    class FakeClient:
        responses = FakeResponses()

    monkeypatch.setattr(
        "src.client.get_llm_client",
        lambda: FakeClient(),
    )

    with pytest.raises(
        RuntimeError,
        match="Groq server error",
    ):
        generate_response(prompt="Test")


def test_generate_response_handles_connection_error(monkeypatch):
    class FakeResponses:
        def create(self, **kwargs):
            raise APIConnectionError(
                request=type(
                    "Request",
                    (),
                    {},
                )(),
            )

    class FakeClient:
        responses = FakeResponses()

    monkeypatch.setattr(
        "src.client.get_llm_client",
        lambda: FakeClient(),
    )

    with pytest.raises(
        RuntimeError,
        match="Could not connect to Groq",
    ):
        generate_response(prompt="Test")
