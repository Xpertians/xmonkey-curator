# tests/test_base_handler.py

from src.xmonkey_curator.base_handler import BaseFileHandler
import tempfile

def test_file_size_eligibility():
    with tempfile.NamedTemporaryFile() as tmpfile:
        # Create a small file and check eligibility
        handler = BaseFileHandler(tmpfile.name)
        assert handler.is_eligible() == True

        # Increase file size beyond the limit and check eligibility
        tmpfile.seek(BaseFileHandler.MAX_SIZE + 1)
        tmpfile.write(b'\0')
        tmpfile.flush()
        assert handler.is_eligible() == False
