from dataclasses import dataclass
import unicodedata

@dataclass
class EvaluationResult:
    """Result of evaluating a model response."""

    case_name: str
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

@dataclass
class EvaluationSummary:
    """Aggregate results from an evaluation run."""

    total_cases: int
    passed_cases: int
    failed_cases: int
    score: float

@dataclass
class EvaluationReport:
    """Complete evaluation report."""

    summary: EvaluationSummary
    total_tokens: int
    model: str
    temperature: float
    run_at: str
    results: list[EvaluationResult]

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
    case_name: str,
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
        case_name=case_name,
        passed=passed,
        expected=expected,
        actual=actual,
        reason=reason
    )

def validate_evaluation_cases(cases: list[dict]) -> None:
    """Validate the structure of evaluation cases."""
    required_fields = {
        "name",
        "context",
        "question",
        "expected"
    }

    if not isinstance(cases, list) :
        raise ValueError("Evaluation cases must be provided as a list.")

    for index, case in enumerate(cases, start = 1):
        if not isinstance(case, dict) :
            raise ValueError(
                "Evaluation cases {index} must be an object."
            )

        missing_fields = required_fields - case.keys()

        if missing_fields:
            missing = ", ".join(sorted(missing_fields))

            raise ValueError(
                f"Evaluation case {index} is missing required field(s): {missing}"
            )

        for field in required_fields:
            value = case[field]

            if not isinstance(value, str) :
                raise ValueError(f"Evaluation cases {index} field '{field}' must be a string.")

            if not value.strip():
                raise ValueError(
                    f"Evaluation case {index} field '{field}' cannot be empty."
                )

def run_evaluation(
    cases: list[EvaluationCase],
) -> list[EvaluationResult]:
    """Run all evaluation cases and return their results."""

    results=[]

    for case in cases:
        result = evaluate_contains(
            case_name=case.name,
            actual=case.actual,
            expected=case.expected,
        )

        results.append(result)
    return results


def summarize_evaluation(
        results: list[EvaluationResult],
) -> EvaluationSummary:
    """Create aggregate metrics from evaluation results."""

    total_cases = len(results)
    passed_cases = sum(result.passed for result in results)
    failed_cases = total_cases - passed_cases

    score = (
        (passed_cases / total_cases) * 100
        if total_cases
        else 0.0
    )

    return EvaluationSummary(
        total_cases=total_cases,
        passed_cases=passed_cases,
        failed_cases=failed_cases,
        score=score
    )
