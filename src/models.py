from dataclasses import dataclass

@dataclass
class TokenUsage:
    """Token usage information for an LLM request."""

    input_tokens: int
    output_tokens: int
    total_tokens: int

@dataclass
class LLMResponse:
    """Response returned by the LLM client."""

    text: str
    usage: TokenUsage

