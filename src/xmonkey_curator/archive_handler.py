import os
import tempfile
import shutil
import zipfile
import tarfile
from .base_handler import BaseFileHandler
from .handler_registry import get_handler

class ArchiveHandler(BaseFileHandler):
    def __init__(self, file_path):
        super().__init__(file_path)

    def process(self):
        """Extracts the archive to a temporary directory, processes each file, then cleans up."""
        with tempfile.TemporaryDirectory() as temp_dir:
            self.extract_archive(temp_dir)
            self.process_directory(temp_dir)

    def extract_archive(self, destination):
        """Extracts the archive to the specified destination directory."""
        if zipfile.is_zipfile(self.file_path):
            with zipfile.ZipFile(self.file_path, 'r') as zip_ref:
                zip_ref.extractall(destination)
        elif tarfile.is_tarfile(self.file_path):
            with tarfile.open(self.file_path, 'r:*') as tar_ref:
                tar_ref.extractall(destination)
        else:
            print(f"Unsupported archive format: {self.file_path}")

    def process_directory(self, directory):
        """Recursively processes each file in the directory."""
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                mime_type, _ = mimetypes.guess_type(file_path)
                handler_class = get_handler(mime_type if mime_type else "application/octet-stream")
                if handler_class:
                    handler = handler_class(file_path)
                    handler.process()
                else:
                    print(f"No handler registered for MIME type: {mime_type} of file {file_path}")
