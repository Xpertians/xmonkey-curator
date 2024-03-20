# tests/test_text_handler.py

from src.xmonkey_curator.handlers.text_handler import TextFileHandler
import tempfile

def test_word_extraction():
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmpfile:
        tmpfile.write("Hello, world! This is a test.")
        tmpfile.flush()

        handler = TextFileHandler(tmpfile.name)
        words = handler.extract_words()
        assert len(words) == 6  # Adjust according to your extraction logic
        assert "Hello" in words
        assert "world" in words
