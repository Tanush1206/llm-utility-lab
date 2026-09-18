import json
from src.evaluation import EvaluationCase, run_evaluation, summarize_evaluation
from src.qa import answer_question
from pathlib import Path

def load_evaluation_cases() -> list[dict]:
    """Load evaluation cases from the JSON file."""

    cases_path = Path(__file__).parent / "evaluation" / "qa_cases.json"
    with cases_path.open(
        "r",
        encoding="utf-8"
    ) as file:
        cases = json.load(file)

        validate_evaluation_cases(cases)

        return cases

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
        if not isinstance(cases, list) :
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

            if not isinstance(cases, list) :
                raise ValueError("Evaluation cases {index} field '{field}' must bea string.")

            if not value.strip(): raise ValueError(
                f"Evaluation case {index} field '{field}' cannot be empty"
            )

def main():
    print("\n=== Q&A Evaluation ===\n")

    evaluation_cases = load_evaluation_cases()

    evaluation_inputs = []
    total_tokens = 0

    for case in evaluation_cases:
        response = answer_question(
            context=case["context"],
            question=case["question"],
        )

        total_tokens += response.usage.total_tokens

        evaluation_inputs.append(
            EvaluationCase(
                name=case["name"], actual=response.text, expected=case["expected"]
            )
        )

    results = run_evaluation(evaluation_inputs)

    summary = summarize_evaluation(results)

    for case, result in zip(evaluation_cases, results):
        status = "✓" if result.passed else "✗"

        print(f"{status} {case['name']}")

        if not result.passed:
            print(f"   Expected: {result.expected}")
            print(f"   Actual:   {result.actual}")

    print("\n--------------------------")
    print(f"Passed: {summary.passed_cases}/{summary.total_cases}")
    print(f"Score: {summary.score:.0f}%")
    print(f"Total tokens: {total_tokens}")


if __name__ == "__main__":
    main()
