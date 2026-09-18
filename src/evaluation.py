from dataclasses import dataclass
import unicodedata

@dataclass
class EvaluationResult:
    """Result of evaluating a model response."""

    passed: bool
    expected: str
    actual: str
    reason: str

@dataclass
class EvaluationCase:
    """A single evaluation case."""

    name: str
    actual: str
    expected: str

def normalize_text(text: str) -> str:
    """Normalize text for reliable evaluation comparisons."""

    text = unicodedata.normalize("NFKC" , text)

    hyphens = {
        "\u2010": "-",
        "\u2011": "-",
        "\u2012": "-",
        "\u2013": "-",
        "\u2014": "-",
        "\u2212": "-",
    }

    for source, replacement in hyphens.items():
        text = text.replace(source, replacement)

    return " ".join(text.strip().lower().split())

def evaluate_contains(
    actual: str,
    expected: str,
)-> EvaluationResult:
    """
    Check whether the model response contains the expected text.
    """

    normalized_actual = normalize_text(actual)
    normalized_expected = normalize_text(expected)

    passed = normalized_expected in normalized_actual

    if passed:
        reason = "Expected text was found in the model response"
    else:
        reason = "Expected text was not found in the model response."

    return EvaluationResult(
        passed=passed,
        expected=expected,
        actual=actual,
        reason=reason
    )


def run_evaluation(
        cases: list[EvaluationCase],
) -> list[EvaluationResult]:
    """Run all evaluation cases and return their results."""

    results=[]

    for case in cases:
        result = evaluate_contains(
            actual=case.actual,
            expected=case.expected,
        )

        results.append(result)
    return results
