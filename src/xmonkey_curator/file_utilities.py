import mimetypes
import magic
import os
import hashlib
import ssdeep
from os import path


class FileUtilities:
    @staticmethod
    def identify_mime_type(file_path):
        if (path.exists(file_path)):
            mime_type, _ = mimetypes.guess_type(file_path)
            if mime_type:
                return mime_type
            else:
                mime = magic.Magic(mime=True)
                mime_type = mime.from_file(file_path)
                if mime_type:
                    return mime_type
                else:
                    return "application/octet-stream"
        else:
            return "application/octet-stream"

    @staticmethod
    def get_file_size(file_path):
        if (path.exists(file_path)):
            return os.path.getsize(file_path)
        else:
            return 0

    @staticmethod
    def calculate_hashes(file_path):
        if (path.exists(file_path)):
            hash_md5 = hashlib.md5()
            hash_sha256 = hashlib.sha256()
            hash_sha1 = hashlib.sha1()
            hash_ssdeep = ''
            with open(file_path, "rb") as f:
                file_content = f.read()
                hash_ssdeep = ssdeep.hash(file_content)
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
                    hash_sha256.update(chunk)
                    hash_sha1.update(chunk)
            return (hash_md5.hexdigest(), hash_sha1.hexdigest(),
                    hash_sha256.hexdigest(), hash_ssdeep)
        else:
            return '', '', '', ''
