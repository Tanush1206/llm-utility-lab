from src.evaluation import EvaluationCase, run_evaluation
from src.qa import answer_question

EVALUATION_CASES = [
    {
        "name" : "Direct factual answer",
        "context": (
            "The company was founded in 2018 and develops "
            "cloud-based accounting software."
        ),
        "question": "When was the company founded?",
        "expected": "2018",
    },
    {
        "name" : "Context-grounded answer",
        "context": (
            "The company was founded in 2018 and develops "
            "cloud-based accounting software."
        ),
        "question": "When does the company develop?",
        "expected": "cloud-based accounting software",
    },
    {
        "name" : "Missing information",
        "context": (
            "The company develops cloud-based accounting software."
        ),
        "question": "Who is the CEO of the company?",
        "expected": "cannot be determined",
    }
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
                name=case["name"],
                actual=response.text,
                expected=case["expected"]
            )
        )

    results = run_evaluation(evaluation_inputs)

    passed_counts = sum(result.passed for result in results)
    total_cases = len(results)

    for case, result in zip(EVALUATION_CASES, results):
        status = "✓" if result.passed else "✗"

        print(f"{status} {case['name']}")

        if not result.passed:
            print(f"   Expected: {result.excepted}")
            print(f"   Actual:   {result.actual}")

    score = (passed_counts / total_cases) * 100 if total_cases else 0

    print("\n--------------------------")
    print(f"Passed: {passed_counts}/{total_cases}")
    print(f"Score: {score:.0f}%")
    print(f"Total tokens: {total_tokens}")

if __name__ == "__main__":
    main()

