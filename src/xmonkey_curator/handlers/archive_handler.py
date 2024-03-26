import os
import bz2
import gzip
import lzma
import magic
import shutil
import rpmfile
import zipfile
import tarfile
import tempfile
import subprocess
from os import path
from tqdm import tqdm
from ..base_handler import BaseFileHandler
from ..file_utilities import FileUtilities


class ArchiveHandler(BaseFileHandler):
    def process(self, process_file_callback):
        with tempfile.TemporaryDirectory() as temp_dir:
            self.extract_archive(temp_dir)
            extracted_files = [
                os.path.join(root, file_name)
                for root, dirnames, files in os.walk(temp_dir)
                for file_name in files
            ]
            desc = f"Extracting {os.path.basename(self.file_path)}"
            for file_path in tqdm(extracted_files, desc=desc[:75]):
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
        elif filetype == 'application/x-bzip2':
            with bz2.BZ2File(self.file_path) as fr:
                with open(destination, "wb") as fw:
                    shutil.copyfileobj(fr, fw)
        elif filetype == 'application/x-xz':
            with lzma.open(self.file_path) as f:
                with open(destination, 'wb') as fout:
                    file_content = f.read()
                    fout.write(file_content)
        elif filetype == 'application/x-rpm':
            with rpmfile.open(self.file_path) as rpm:
                for entry in rpm.getmembers():
                    file_path = os.path.join(destination, entry.name)
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    with open(file_path, 'wb') as f_out, \
                            rpm.extractfile(entry) as f_in:
                        f_out.write(f_in.read())
        elif filetype == 'application/x-debian-package':
            destination = os.path.abspath(destination)
            os.makedirs(destination, exist_ok=True)
            file_path = os.path.abspath(self.file_path)
            cmd = f"ar -x {file_path}"
            if (path.exists(file_path)):
                process = subprocess.Popen(
                    cmd,
                    cwd=destination,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE)
                (result, error) = process.communicate()
                if process.returncode != 0:
                    print(f"Error extracting .deb package: {error.decode()}")
                    return
                rc = process.wait()
                process.stdout.close()
                data_archives = [
                    f for f in os.listdir(destination)
                    if f.startswith('data.tar')
                ]
                for data_archive in data_archives:
                    data_archive_path = os.path.join(destination, data_archive)
                    with tarfile.open(data_archive_path) as data:
                        data.extractall(path=destination)
        else:
            raise ValueError(f"Unsupported archive format: {self.file_path}")
