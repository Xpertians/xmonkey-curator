import re
import os
import logging
from ..base_handler import BaseFileHandler
from pygments import lex
from pygments.lexers import get_lexer_by_name


class JvmFileHandler(BaseFileHandler):
    def __init__(self, file_path):
        """
        Initializes the handler with a specific file path.
        """
        super().__init__(file_path)
        self.logger = logging.getLogger(__name__)
        self.file_path = file_path

    def extract_words(self):
        symbols = []
        base_name = os.path.basename(self.file_path)
        file_name = os.path.splitext(base_name)[0]
        symbols.append(file_name.lower())
        words = list(set(symbols))
        regex = re.compile(r'[^a-zA-Z\s_-]+')
        words = [
            regex.sub('', word).strip() for word in words
            if len(regex.sub('', word).strip()) >= 5
        ]
        return words
