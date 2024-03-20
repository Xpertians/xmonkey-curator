import click
import logging
import os
import mimetypes
from xmonkey_curator.handler_registry import get_handler
from xmonkey_curator.report_generator import ReportGenerator
from xmonkey_curator.handlers.archive_handler import ArchiveHandler
from xmonkey_curator.file_utilities import FileUtilities


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@click.command()
@click.argument('path', type=click.Path(exists=True))
def scan(path):
    """
    Scans a given file or recursively scans a directory for files to process.
    """
    results = []
    if os.path.isdir(path):
        logger.info(f"Scanning directory: {path}")
        for root, _, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                result = process_file(file_path, results)
                if result:
                    results.append(result)
    else:
        logger.info(f"Scanning file: {path}")
        result = process_file(path, results)
        if result:
            results.append(result)
    report_generator = ReportGenerator(results)
    report_generator.print_report()  # or report_generator.save_report('scan_report.json')

def process_file(file_path, results):
    """
    Processes a single file using the appropriate handler based on its MIME type.
    Returns a dictionary with file processing result or None if no handler is found.
    """
    mime_type = FileUtilities.identify_mime_type(file_path)
    file_size = FileUtilities.get_file_size(file_path)
    checksum = FileUtilities.calculate_checksum(file_path)
    if mime_type in ['application/zip', 'application/gzip', 'application/x-tar']:
        handler = ArchiveHandler(file_path)
        handler.process(lambda path: process_file(path, results))
    else:
        handler_class = get_handler(mime_type if mime_type else "application/octet-stream")
        if handler_class:
            handler = handler_class(file_path)
            if isinstance(handler, ArchiveHandler):
                handler.process(lambda path: process_file(path, results))
            else:
                print("file:"+file_path+", mime:"+mime_type)
                words = handler.extract_words()
                result = {
                    'file_path': file_path,
                    'mime_type': mime_type,
                    'size': file_size,
                    'checksum': checksum,
                    'words': words,
                }
                results.append(result)
        else:
            logger.info(f"No handler registered for MIME type: {mime_type} for file {file_path}")
            return None

if __name__ == '__main__':
    scan()
