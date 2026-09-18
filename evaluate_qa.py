from src.evaluation import EvaluationCase, run_evaluation, summarize_evaluation
from src.qa import answer_question


EVALUATION_CASES = [
    {
        "name": "Direct factual answer",
        "context": (
            "The company was founded in 2018 and develops "
            "cloud-based accounting software."
        ),
        "question": "When was the company founded?",
        "expected": "2018",
    },
    {
        "name": "Context-grounded answer",
        "context": (
            "The company was founded in 2018 and develops "
            "cloud-based accounting software."
        ),
        "question": "What does the company develop?",
        "expected": "cloud-based accounting software",
    },
    {
        "name": "Missing information",
        "context": ("The company develops cloud-based accounting software."),
        "question": "Who is the CEO of the company?",
        "expected": "cannot be determined",
    },
]


def main():
    print("\n=== Q&A Evaluation ===\n")

    evaluation_inputs = []

    total_tokens = 0

    for case in EVALUATION_CASES:
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

    for case, result in zip(EVALUATION_CASES, results):
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
