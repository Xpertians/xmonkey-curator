import os
import tempfile
import shutil
import bz2
import gzip
import lzma
import magic
import shutil
import zipfile
import tarfile
from ..base_handler import BaseFileHandler
from ..file_utilities import FileUtilities


class ArchiveHandler(BaseFileHandler):
    def process(self, process_file_callback):
        with tempfile.TemporaryDirectory() as temp_dir:
            self.extract_archive(temp_dir)
            for root, _, files in os.walk(temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    process_file_callback(file_path)

    def extract_archive(self, destination):
        """Extracts the archive to the specified destination directory."""
        filetype = FileUtilities.identify_mime_type(self.file_path)
        # print('mime:', filetype)
        if zipfile.is_zipfile(self.file_path):
            with zipfile.ZipFile(self.file_path, 'r') as zip_ref:
                zip_ref.extractall(destination)
        elif tarfile.is_tarfile(self.file_path):
            with tarfile.open(self.file_path, 'r:*') as tar_ref:
                tar_ref.extractall(destination)
        elif filetype in 'application/gzip':
            base_name = os.path.basename(self.file_path)
            file_name = os.path.splitext(base_name)[0]
            with gzip.open(self.file_path, 'rb') as f_in:
                dest_file = destination+"/"+file_name
                with open(dest_file, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
        elif filetype in 'application/x-bzip2':
            print('bunzip2:', self.file_path)
            with bz2.BZ2File(self.file_path) as fr, open(destination, "wb") as fw:
                shutil.copyfileobj(fr, fw)
        elif filetype in 'application/x-xz':
            with lzma.open(self.file_path) as f, open(destination, 'wb') as fout:
                file_content = f.read()
                fout.write(file_content)
        else:
            raise ValueError(f"Unsupported archive format: {self.file_path}")
