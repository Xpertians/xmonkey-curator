import re
import os
import logging
from ..base_handler import BaseFileHandler
from ..lexer_utilities import LexerUtilities


class CplusFileHandler(BaseFileHandler):
    def __init__(self, file_path):
        """
        Initializes the handler with a specific file path.
        """
        super().__init__(file_path)
        self.logger = logging.getLogger(__name__)
        self.file_path = file_path

    def extract_words(self):
        words = []
        try:
            with open(self.file_path, 'r') as file:
                source_code = file.read()
                words = LexerUtilities.lexer('cpp', source_code)
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except Exception as e:
            print(f"Error processing file: {e}")
        base_name = os.path.basename(self.file_path)
        file_name = os.path.splitext(base_name)[0]
        words.append(file_name.lower())
        return words
