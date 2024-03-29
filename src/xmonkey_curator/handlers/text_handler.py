import logging
import re
from ..base_handler import BaseFileHandler
from ..lexer_utilities import LexerUtilities


class TextFileHandler(BaseFileHandler):
    def __init__(self, file_path):
        super().__init__(file_path)
        self.logger = logging.getLogger(__name__)

    def extract_words(self):
        """Extracts words from the text file."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                words = re.findall(r'\b\w{5,}\b', content.lower())
                words = list(set(words))
                return words
        except Exception as e:
            self.logger.error(
                 f"Failed to process text file {self.file_path}: {e}")
            self.logger.warning(
                 f"No strings extracted from {self.file_path}."
                 )
            # Using file data
            words = LexerUtilities.get_strings(self.file_path)
            if words:
                words = LexerUtilities.clean_strings(words)
                return words
            return []
