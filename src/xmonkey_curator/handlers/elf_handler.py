import os
import re
import lief
import logging
from ..base_handler import BaseFileHandler
from ..lexer_utilities import LexerUtilities


class ElfFileHandler(BaseFileHandler):
    def __init__(self, file_path):
        super().__init__(file_path)
        self.logger = logging.getLogger(__name__)

    def extract_words(self):
        if not self.is_eligible():
            return []
        try:
            elf = lief.parse(self.file_path)
            words = []
            for section in elf.sections:
                if section.name == ".rodata":
                    data = section.content
                    words = self._extract_strings_from_data(data)
            words = LexerUtilities.clean_strings(words)
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

    def _extract_strings_from_data(self, data):
        """A utility method to extract strings from binary data."""
        strings = []
        current_str = []
        for byte in data:
            if 32 <= byte <= 127:  # Printable ASCII range
                current_str.append(chr(byte))
            elif current_str:
                strings.append(''.join(current_str))
                current_str = []
        if current_str:  # Add the last string if any
            strings.append(''.join(current_str))
        return strings
