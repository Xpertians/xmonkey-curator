import logging
import re
from ..base_handler import BaseFileHandler

class TextFileHandler(BaseFileHandler):
    def __init__(self, file_path):
        super().__init__(file_path)
        self.logger = logging.getLogger(__name__)

    def extract_words(self):
        """Extracts words from the text file."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                words = re.findall(r'\b\w{3,}\b', content)
                filtered_words = [word for word in words if word.isalnum()]
                return filtered_words
        except Exception as e:
            self.logger.error(f"Failed to process text file {self.file_path}: {e}")
            return []
