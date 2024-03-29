import mimetypes
import magic
import os
import hashlib
import ssdeep
from os import path
import subprocess


class FileUtilities:
    @staticmethod
    def identify_mime_type(file_path):
        if (path.exists(file_path)):
            mime_typeA, _ = mimetypes.guess_type(file_path)
            mime = magic.Magic(uncompress=True, mime=True)
            mime_typeB = mime.from_file(file_path)
            mime_type = "application/octet-stream"
            if mime_typeA == "application/octet-stream":
                if mime_typeB == "application/octet-stream":
                    res = subprocess.run(
                        ["file", "--mime-type", "--brief", file_path],
                        stdout=subprocess.PIPE
                    )
                    if res.stdout:
                        mime_type = res.stdout.decode("utf-8")
                    else:
                        mime_type = mime_typeB
                elif mime_typeB:
                    mime_type = mime_typeB
                else:
                    res = subprocess.run(
                        ["file", "--mime-type", "--brief", file_path],
                        stdout=subprocess.PIPE
                    )
                    if res.stdout:
                        mime_type = res.stdout.decode("utf-8")
                    else:
                        mime_type = "application/octet-stream"
            elif mime_typeA:
                mime_type = mime_typeA
            else:
                res = subprocess.run(
                    ["file", "--mime-type", "--brief", file_path],
                    stdout=subprocess.PIPE
                )
                if res.stdout:
                    mime_type = res.stdout.decode("utf-8")
                else:
                    mime_type = "application/octet-stream"
            return mime_type.strip()
        else:
            return "ERR/file-not-found"

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
