import click
import logging
import os
import mimetypes
from xmonkey_curator.handler_registry import get_handler

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@click.command()
@click.argument('path', type=click.Path(exists=True), help="The path to a file or directory to scan.")
def scan(path):
    """
    Scans a given file or recursively scans a directory for files to process.
    
    PATH: A path to a file or directory that you want to scan. If a directory is provided, 
    all files within the directory (and its subdirectories) will be scanned recursively.
    """
    if os.path.isdir(path):
        logger.info(f"Scanning directory: {path}")
        for root, _, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                process_file(file_path)
    else:
        logger.info(f"Scanning file: {path}")
        process_file(path)

def process_file(file_path):
    """
    Processes a single file using the appropriate handler based on its MIME type.
    """
    mime_type, _ = mimetypes.guess_type(file_path)
    handler = get_handler(file_path, mime_type if mime_type else "application/octet-stream")
    words = handler.extract_words()
    logger.info(f"Processed {file_path}: {len(words)} words extracted")

if __name__ == '__main__':
    scan()
