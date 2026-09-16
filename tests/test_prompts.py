from src.summarizer import summarize_text
from src.qa import answer_question


def test_summarizer_rejects_empty_text():
    try :
        summarize_text("")
        assert False, "Expected ValueError for empty text"
    except ValueError:
        pass

def test_summarizer_rejects_whitespace():
    try:
        summarize_text("     ")
        assert False, "Expected ValueError for whitespace_only text"
    except ValueError:
        pass

def test_qa_rejects_empty_context():
    try :
        answer_question("", "What is the answer?")
        assert False, "Expected ValueError for empty text"
    except ValueError:
        pass

def test_qa_rejects_empty_question():
    try:
        answer_question("Some useful context.", "")
        assert False, "Expected ValueError for whitespace_only text"
    except ValueError:
        pass
