import re
import logging
from os import path
from ..base_handler import BaseFileHandler
from ..lexer_utilities import LexerUtilities


class OctetStreamFileHandler(BaseFileHandler):
    def __init__(self, file_path):
        super().__init__(file_path)
        self.logger = logging.getLogger(__name__)

    def extract_words(self):
        min_length = 5
        if (path.exists(self.file_path)):
            with open(self.file_path, 'rb') as file:
                content = file.read()
            text = ''
            strings = []
            for byte in content:
                try:
                    char = byte.to_bytes(1, 'big').decode('utf-8')
                    if char.isprintable():
                        text += char
                        continue
                except UnicodeDecodeError:
                    pass
                if len(text) >= min_length:
                    strings.append(text)
                text = ''
            words = LexerUtilities.clean_strings(strings)
            return words
        else:
            return []
