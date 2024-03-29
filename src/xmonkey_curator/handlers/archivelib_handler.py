import re
import logging
import subprocess
from os import path
from ..base_handler import BaseFileHandler
from ..lexer_utilities import LexerUtilities


class ArchiveLibFileHandler(BaseFileHandler):
    def __init__(self, file_path):
        super().__init__(file_path)
        self.logger = logging.getLogger(__name__)

    def extract_words(self):
        min_length = 5
        strings = []
        if (path.exists(self.file_path)):
            # Extracting using AR
            cmd = 'ar -t ' + self.file_path
            process = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
            (result, error) = process.communicate()
            rc = process.wait()
            process.stdout.close()
            rstTXT = result.decode('utf-8').replace('/', '')
            strings = re.compile(r'\W+', re.UNICODE).split(
                ' '.join(rstTXT.split()))
            words = LexerUtilities.clean_strings(strings)
            # Using file data
            strings = LexerUtilities.get_strings(self.file_path)
            if strings:
                words = strings+words
                words = LexerUtilities.clean_strings(words)
            return words
        else:
            return []
