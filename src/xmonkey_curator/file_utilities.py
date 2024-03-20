import mimetypes


mimetypes.add_type('text/markdown', '.md')


class FileUtilities:
    @staticmethod
    def identify_mime_type(file_path):
        mime_type, _ = mimetypes.guess_type(file_path)
        return mime_type or "application/octet-stream"

    @staticmethod
    def calculate_checksum(file_path):
        # Implementation for calculating file checksum
        pass
