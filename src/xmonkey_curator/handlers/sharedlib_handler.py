import os
import re
import lief
import logging
from ..base_handler import BaseFileHandler
from ..lexer_utilities import LexerUtilities


class SharedLibFileHandler(BaseFileHandler):
    def __init__(self, file_path):
        super().__init__(file_path)
        self.logger = logging.getLogger(__name__)

    def extract_words(self):
        if not self.is_eligible():
            return []
        try:
            libSO = lief.parse(self.file_path)
            words = []
            iter = filter(lambda e: e.exported, libSO.dynamic_symbols)
            for idx, lsym in enumerate(iter):
                words.append(lsym.name)
            words = list(set(words))
            if not words:
                self.logger.warning(
                     f"No strings extracted from {self.file_path}."
                     )
                # Using file data
                strings = LexerUtilities.get_strings(self.file_path)
                if strings:
                    words = strings+words
                    words = LexerUtilities.clean_strings(words)
            return words
        except Exception as e:
            self.logger.error(
                 f"Error processing Shared Lib file {self.file_path}: {e}"
                 )
            return []
