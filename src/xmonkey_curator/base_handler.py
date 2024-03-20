import logging

class BaseFileHandler:
    def __init__(self, file_path):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.file_path = file_path

    def is_eligible(self):
        if os.path.getsize(self.file_path) > BaseFileHandler.MAX_SIZE:
            self.logger.info(f'File skipped (size > 1MB): {self.file_path}')
            return False
        return True
