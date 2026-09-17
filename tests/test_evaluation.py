from src.evaluation import evaluate_contains

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
