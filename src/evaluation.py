from dataclasses import dataclass

@dataclass
class EvaluationResult:
    """Result of evaluating a model response."""

    passed: bool
    excepted: str
    actual: str
    reason: str


def evaluate_contains(
    actual: str,
    expected: str,
)-> EvaluationResult:
    """
    Check whether the model response contains the expected text.
    """

    normalized_actual = actual.strip().lower()
    normalized_expected= expected.strip().lower()

    passed = normalized_expected in normalized_actual

    if passed:
        reason = "Expected text was found in the model response"
    else:
        reason = "Expected text was not found in the model response."

    return EvaluationResult(
        passed=passed,
        excepted=expected,
        actual=actual,
        reason=reason
    )
