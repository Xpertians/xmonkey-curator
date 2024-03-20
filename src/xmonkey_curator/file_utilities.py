import mimetypes
import os
import hashlib


class FileUtilities:
    @staticmethod
    def identify_mime_type(file_path):
        mime_type, _ = mimetypes.guess_type(file_path)
        return mime_type or "application/octet-stream"

    @staticmethod
    def get_file_size(file_path):
        """Get the file size in bytes."""
        return os.path.getsize(file_path)

    @staticmethod
    def calculate_checksum(file_path):
        """Calculate the MD5 checksum of a file."""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
