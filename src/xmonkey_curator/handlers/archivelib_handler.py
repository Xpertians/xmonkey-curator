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
            words = list(set(strings))
            regex = re.compile(r'[^a-zA-Z\s_-]+')
            words = [
                regex.sub('', word).strip() for word in words
                if len(regex.sub('', word).strip()) >= 5
            ]
            # Using file data
            strings = LexerUtilities.get_strings(self.file_path)
            if strings:
                words = strings+words
                words = list(set(words))
                regex = re.compile(r'[^a-zA-Z\s_-]+')
                words = [
                    regex.sub('', word).strip() for word in words
                    if len(regex.sub('', word).strip()) >= 5
                ]
            return words
        else:
            return [] 
