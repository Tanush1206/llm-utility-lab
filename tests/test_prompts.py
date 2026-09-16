from src.summarizer import summarize_text

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
