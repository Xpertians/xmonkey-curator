# archive_handler.py

import os
import tempfile
import shutil
import zipfile
import tarfile
from ..base_handler import BaseFileHandler


class ArchiveHandler(BaseFileHandler):
    def process(self, process_file_callback):
        """Extracts the archive and processes its contents."""
        with tempfile.TemporaryDirectory() as temp_dir:
            self.extract_archive(temp_dir)
            # Process each file in the temporary directory
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    process_file_callback(file_path)
            # Temporary directory and its contents are automatically cleaned up

    def extract_archive(self, destination):
        """Extracts the archive to the specified destination directory."""
        if zipfile.is_zipfile(self.file_path):
            with zipfile.ZipFile(self.file_path, 'r') as zip_ref:
                zip_ref.extractall(destination)
        elif tarfile.is_tarfile(self.file_path):
            with tarfile.open(self.file_path, 'r:*') as tar_ref:
                tar_ref.extractall(destination)
        else:
            raise ValueError(f"Unsupported archive format: {self.file_path}")
