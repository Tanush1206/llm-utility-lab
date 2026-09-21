import json
from pathlib import Path
from src.client import get_default_model, get_default_temperature
from datetime import datetime, timezone
from src.prompts import QA_PROMPT_VERSION

from src.evaluation import (
    EvaluationCase,
    EvaluationReport,
    EvaluationSummary,
    compare_evaluation_runs,
    run_evaluation,
    summarize_evaluation,
    validate_evaluation_cases,
)
from src.qa import answer_question


def load_evaluation_cases() -> list[dict]:
    """Load evaluation cases from the JSON file."""

    cases_path = Path(__file__).parent / "evaluation" / "qa_cases.json"
    with cases_path.open("r", encoding="utf-8") as file:
        cases = json.load(file)

        validate_evaluation_cases(cases)

        return cases


def load_previous_evaluation_report(
    history_dir: Path,
) -> EvaluationReport | None:
    """Load the most recent historical evaluation report."""

    history_files = sorted(
        history_dir.glob("report_*.json"),
        reverse=True,
    )

    if not history_files:
        return None

    with history_files[0].open("r", encoding="utf-8") as file:
        data = json.load(file)

    summary = data["summary"]

    return EvaluationReport(
        summary=EvaluationSummary(
            total_cases=summary["total_cases"],
            passed_cases=summary["passed_cases"],
            failed_cases=summary["failed_cases"],
            score=summary["score"],
        ),
        total_tokens=data["total_tokens"],
        model=data["model"],
        temperature=data["temperature"],
        run_at=data["run_at"],
        prompt_version=data["prompt_version"],
        results=[],
    )


def save_evaluation_report(
    report: EvaluationReport,
    report_path: Path | None = None,
) -> None:
    """Save the evaluation report as a JSON file."""

    if report_path is None:
        report_path = Path(__file__).parent / "evaluation" / "latest_report.json"

    history_dir = report_path.parent / "history"
    history_dir.mkdir(parents=True, exist_ok=True)

    report_data = {
        "summary": {
            "total_cases": report.summary.total_cases,
            "passed_cases": report.summary.passed_cases,
            "failed_cases": report.summary.failed_cases,
            "score": report.summary.score,
        },
        "total_tokens": report.total_tokens,
        "model": report.model,
        "temperature": report.temperature,
        "run_at": report.run_at,
        "prompt_version": report.prompt_version,
        "results": [
            {
                "case_name": result.case_name,
                "passed": result.passed,
                "expected": result.expected,
                "actual": result.actual,
                "reason": result.reason,
            }
            for result in report.results
        ],
    }

    with report_path.open("w", encoding="utf-8") as file:
        json.dump(report_data, file, indent=2)

    history_filename = (
        f"report_{report.run_at.replace(':', '').replace('+00.00', 'Z')}.json"
    )

    history_path = history_dir / history_filename

    with history_path.open("w", encoding="utf-8") as file:
        json.dump(report_data, file, indent=2)


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

    report = EvaluationReport(
        summary=summary,
        total_tokens=total_tokens,
        model=get_default_model(),
        temperature=get_default_temperature(),
        run_at=datetime.now(timezone.utc).isoformat(),
        prompt_version=QA_PROMPT_VERSION,
        results=results,
    )

    history_dir = Path(__file__).parent / "evaluation" / "history"

    previous_report = load_previous_evaluation_report(history_dir)

    if previous_report:
        comparison = compare_evaluation_runs(previous=previous_report, current=report)

        print("\n=== Evaluation Comparison ===")
        print(f"Score change: {comparison.score_change:+.2f}%")
        print(f"Token change: {comparison.token_change:+d}")
        print(f"Passed cases change: {comparison.passed_cases_change:+d}")
        print(f"Failed cases change: {comparison.failed_cases_change:+d}")

    save_evaluation_report(report)

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
