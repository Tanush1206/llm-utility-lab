from src.evaluation import evaluate_contains
from src.evaluation import EvaluationCase, EvaluationResult, evaluate_contains, run_evaluation, summarize_evaluation


def test_evaluation_passes_expected_text_is_present():
    result = evaluate_contains(
        actual="The company was founded in 2018.",
        expected="2018",
    )

    assert result.passed is True


def test_evaluation_fails_when_expected_text_is_missing():
    result = evaluate_contains(
        actual="The company was founded in 2020.",
        expected="2018",
    )

    assert result.passed is False


def test_evaluation_is_case_insensitive():
    result = evaluate_contains(
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
        actual="The company develops cloud\u2011based accounting software.",
        expected="cloud-based accounting software",
    )

    assert result.passed is True


def test_summarize_evaluation_calculates_metrics():
    results = [
        EvaluationResult(
            passed=True,
            expected="2018",
            actual="The company was founded in 2018.",
            reason="Expected text was found in the model response."
        ),
        EvaluationResult(
            passed=True,
            expected="software",
            actual="The company develops software.",
            reason="Expected text was found in the model response."
        ),
        EvaluationResult(
            passed=False,
            expected="India",
            actual="The company is based in Germany",
            reason="Expected text was found in the model response."
        ),
    ]

    summary = summarize_evaluation(results)

    assert summary.total_cases == 3
    assert summary.passed_cases == 2
    assert summary.failed_cases == 1
    assert summary.score == 66.66666666666666


