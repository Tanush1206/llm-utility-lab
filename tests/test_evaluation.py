from src.evaluation import (
    EvaluationCase,
    EvaluationResult,
    EvaluationReport,
    evaluate_contains,
    run_evaluation,
    summarize_evaluation,
)
from evaluate_qa import load_evaluation_cases, validate_evaluation_cases, save_evaluation_report


def test_evaluation_passes_expected_text_is_present():
    result = evaluate_contains(
        case_name="Founded year",
        actual="The company was founded in 2018.",
        expected="2018",
    )

    assert result.passed is True


def test_evaluation_fails_when_expected_text_is_missing():
    result = evaluate_contains(
        case_name="Incorrect year",
        actual="The company was founded in 2020.",
        expected="2018",
    )

    assert result.passed is False


def test_evaluation_is_case_insensitive():
    result = evaluate_contains(
        case_name="Case insensitive",
        actual="The company develops Cloud-Based Accounting Software.",
        expected="cloud-based accounting software",
    )

    assert result.passed is True


def test_run_evaluation_passes_all_cases():
    cases = [
        EvaluationCase(
            name="Founded year",
            actual="The company was founded in 2018.",
            expected="2018",
        ),
        EvaluationCase(
            name="Product",
            actual="The company developes cloud-based accounting software.",
            expected="cloud-based accounting software",
        ),
    ]

    results = run_evaluation(cases)

    assert len(results) == 2
    assert all(result.passed for result in results)


def test_run_evaluation_detects_failed_case():
    cases = [
        EvaluationCase(
            name="Incorrect year",
            actual="The company was founded in 2020.",
            expected="2018",
        )
    ]

    results = run_evaluation(cases)

    assert len(results) == 1
    assert results[0].passed is False


def test_run_evaluation_handles_empty_cases():
    results = run_evaluation([])

    assert results == []


def test_evaluation_handles_unicode_hyphens():
    result = evaluate_contains(
        case_name="Unicode hyphen",
        actual="The company develops cloud\u2011based accounting software.",
        expected="cloud-based accounting software",
    )

    assert result.passed is True


def test_summarize_evaluation_calculates_metrics():
    results = [
        EvaluationResult(
            case_name="Founded year",
            passed=True,
            expected="2018",
            actual="The company was founded in 2018.",
            reason="Expected text was found in the model response.",
        ),
        EvaluationResult(
            case_name="Product",
            passed=True,
            expected="software",
            actual="The company develops software.",
            reason="Expected text was found in the model response.",
        ),
        EvaluationResult(
            case_name="Incorrect location",
            passed=False,
            expected="India",
            actual="The company is based in Germany",
            reason="Expected text was found in the model response.",
        ),
    ]

    summary = summarize_evaluation(results)

    assert summary.total_cases == 3
    assert summary.passed_cases == 2
    assert summary.failed_cases == 1
    assert summary.score == 66.66666666666666


def test_load_evaluation_cases():
    cases = load_evaluation_cases()

    assert len(cases) == 3
    assert cases[0]["name"] == "Direct factual answer"
    assert cases[0]["question"] == "When was the company founded?"
    assert cases[0]["expected"] == "2018"


def test_validate_evaluation_cases_accepts_valid_cases():
    cases = [
        {
            "name": "Test case",
            "context": "Some context.",
            "question": "Some question?",
            "expected": "Some answer",
        }
    ]

    validate_evaluation_cases(cases)


def test_validate_evaluation_cases_rejects_missing_fields():
    cases = [
        {
            "name": "Test case",
            "context": "Some context.",
            "question": "Some question?",
        }
    ]

    try:
        validate_evaluation_cases(cases)
        assert False, "Expected ValueError for missing field"
    except ValueError as error:
        assert "expected" in str(error)


def test_validate_evaluation_cases_rejects_non_list():
    try:
        validate_evaluation_cases({"name": "Invalid"})
        assert False, "Expected ValueError for non-list input"
    except ValueError as error:
        assert "must be provided as a list" in str(error)


def test_validate_evaluation_cases_rejects_non_string_field():
    cases = [
        {
            "name": "Test case",
            "context": "Some context.",
            "question": "Some question?",
            "expected": 2018,
        }
    ]

    try:
        validate_evaluation_cases(cases)
        assert False, "Expected ValueError for non-string field"
    except ValueError as error:
        assert "must be a string" in str(error)

def test_validate_evaluation_cases_rejects_empty_field():
    cases = [
        {
            "name": "Test case",
            "context": "Some context.",
            "question": "",
            "expected": "Some answer",
        }
    ]

    try:
        validate_evaluation_cases(cases)
        assert False, "Expected ValueError for empty field"
    except ValueError as error:
        assert "cannot be empty" in str(error)


def test_save_evaluation_report(tmp_path):
    results = [
        EvaluationResult(
            case_name="Founded year",
            passed=True,
            expected="2018",
            actual="2018",
            reason="Expected text was found in the model response",
        )
    ]

    summary = summarize_evaluation(results)

    report = EvaluationReport(
        summary=summary,
        total_tokens=100,
        model="openai/gpt-oss-20b",
        temperature=0.1,
        run_at="2026-09-18T19:00:00+05:30",
        prompt_version="qa-v1",
        results=results
    )

    report_path = tmp_path / "report.json"

    save_evaluation_report(report, report_path)
