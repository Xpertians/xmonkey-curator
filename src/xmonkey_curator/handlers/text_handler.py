import logging
from .base_handler import BaseFileHandler

class TextFileHandler(BaseFileHandler):
    def __init__(self, file_path):
        super().__init__(file_path)
        self.logger = logging.getLogger(__name__)

    def process(self):
        """Process a text file to extract words or other information."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                # Simple example: count words in the text
                words = content.split()
                self.logger.info(f"Found {len(words)} words in {self.file_path}")
                # Add more specific text processing logic here as needed
        except Exception as e:
            self.logger.error(f"Failed to process text file {self.file_path}: {e}")
