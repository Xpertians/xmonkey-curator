import logging
import re
from ..base_handler import BaseFileHandler
from ..CtagsHandler import CtagsHandler

class RubyFileHandler(BaseFileHandler):
    def __init__(self, file_path):
        """
        Initializes the handler with a specific file path.
        """
        super().__init__(file_path)
        self.logger = logging.getLogger(__name__)
        self.file_path = file_path

    def extract_words(self):
        """
        Processes a Ruby file using Ctags to extract symbols like classes and functions.
        """
        ctags = CtagsHandler(self.file_path)
        ctags.setLang('ruby')
        ctags.setLangMap('ruby:+.rake')
        symbols = ctags.run()
        words = list(set(symbols.lower().split(',')))
        return words