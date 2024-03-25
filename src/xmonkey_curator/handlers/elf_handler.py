import lief
import os
from ..base_handler import BaseFileHandler
import logging


class ElfFileHandler(BaseFileHandler):
    def __init__(self, file_path):
        super().__init__(file_path)
        self.logger = logging.getLogger(__name__)

    def extract_words(self):
        """Extract strings from an ELF file using LIEF."""
        if not self.is_eligible():
            return []
        try:
            elf = lief.parse(self.file_path)
            strings = []
            for section in elf.sections:
                if section.name == ".rodata":
                    data = section.content
                    strings.extend(self._extract_strings_from_data(data))
            if not strings:
                self.logger.warning(
                     f"No strings extracted from {self.file_path}."
                     )
            return strings
        except lief.exception as e:
            self.logger.error(
                 f"Error processing ELF file {self.file_path}: {e}"
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
