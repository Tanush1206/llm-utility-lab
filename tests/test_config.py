import pytest

from src.config import (
    DEFAULT_GROQ_MODEL,
    DEFAULT_GROQ_TEMPERATURE,
    get_groq_api_key,
    get_groq_model,
    get_groq_temperature,
)

def test_get_groq_api_key_returns_configured_key(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "test-api-key")

    assert get_groq_api_key() == "test-api-key"

def test_get_groq_api_key_rejects_missing_key(monkeypatch):
    monkeypatch.delenv("GROQ_API_KEY", raising = False)

    with pytest.raises(ValueError, match="GROQ_API_KEY is not set"):
        get_groq_api_key()

def test_get_groq_api_key_rejects_blank_key(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY"," ")

    with pytest.raises(ValueError, match="GROQ_API_KEY is not set. Add it to your .env file."):
        get_groq_api_key()

def test_get_groq_model_returns_configured_model(monkeypatch):
    monkeypatch.setenv("GROQ_MODEL", "test-model")

    assert get_groq_model() == "test-model"

def test_get_groq_model_uses_default(monkeypatch):
    monkeypatch.delenv("GROQ_MODEL", raising = False)

    assert get_groq_model() == DEFAULT_GROQ_MODEL

def test_get_groq_model_rejects_blank_model(monkeypatch):
    monkeypatch.setenv("GROQ_MODEL", " ")

    with pytest.raises(ValueError, match="GROQ_MODEL cannot be empty"):
        get_groq_model()

def test_get_groq_temperature_returns_configured_value(monkeypatch):
    monkeypatch.setenv("GROQ_TEMPERATURE", "0.7")

    assert get_groq_temperature() == 0.7


def test_get_groq_temperature_uses_default(monkeypatch):
    monkeypatch.delenv("GROQ_TEMPERATURE", raising=False)

    assert get_groq_temperature() == DEFAULT_GROQ_TEMPERATURE


def test_get_groq_temperature_rejects_invalid_value(monkeypatch):
    monkeypatch.setenv("GROQ_TEMPERATURE", "invalid")

    with pytest.raises(
        ValueError,
        match="GROQ_TEMPERATURE must be a valid number",
    ):
        get_groq_temperature()


def test_get_groq_temperature_rejects_out_of_range_value(monkeypatch):
    monkeypatch.setenv("GROQ_TEMPERATURE", "2.1")

    with pytest.raises(
        ValueError,
        match="GROQ_TEMPERATURE must be between 0 and 2",
    ):
        get_groq_temperature()
