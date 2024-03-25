import click
import logging
import os
import mimetypes
from xmonkey_curator.handler_registry import get_handler
from xmonkey_curator.report_generator import ReportGenerator
from xmonkey_curator.handlers.archive_handler import ArchiveHandler
from xmonkey_curator.file_utilities import FileUtilities


logging.basicConfig(
    filename='debug.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

EXCLUDED_MIME_TYPE_PREFIXES = [
    'image/',
    'video/',
    'audio/',
]

EXCLUDED_MIME_TYPES = [
    'application/pgp-signature',
    'application/x-font-type1',
]

ARCHIVE_MIME_TYPES = [
    'application/zip',
    'application/gzip',
    'application/x-tar',
    'application/java-archive',
]

@click.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--force-text', is_flag=True, help="Force the use of StringExtract for all files.")
@click.option('--skip-extraction', is_flag=True, help="Skip extracting files from archives.")
@click.option('--print-report', is_flag=True, help="Print the report instead of saving to JSON.")
def scan(path, force_text, skip_extraction, print_report):
    """
    Scans a given file or recursively scans a directory for files to process.
    """
    results = []
    if os.path.isdir(path):
        logger.info(f"Scanning directory: {path}")
        for root, _, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                result = process_file(file_path, results, '', force_text, skip_extraction)
                if result:
                    results.append(result)
    else:
        logger.info(f"Scanning file: {path}")
        result = process_file(path, results, '', force_text, skip_extraction)
        if result:
            results.append(result)
    report_generator = ReportGenerator(results)
    if print_report:
        report_generator.print_report()
    else:
        report_generator.save_report('scan_report.json')


def process_file(file_path, results, archive_checksum=None, force_text=False, skip_extraction=False):
    """
    Processes a single file using the appropriate
    handler based on its MIME type.
    Returns a dictionary with file processing result
    or None if no handler is found.
    """
    mime_type = FileUtilities.identify_mime_type(file_path)
    file_size = FileUtilities.get_file_size(file_path)
    hash_md5, hash_sha1, hash_sha256, hash_ssdeep = FileUtilities.calculate_hashes(file_path)
    if mime_type in EXCLUDED_MIME_TYPES:
        logger.info(f"Skipping excluded MIME type: {mime_type} for file {file_path}")
        return None
    elif any(mime_type.startswith(prefix) for prefix in EXCLUDED_MIME_TYPE_PREFIXES):
        logger.info(f"Skipping excluded MIME type: {mime_type} for file {file_path}")
        return None
    elif mime_type in ARCHIVE_MIME_TYPES:
        if not skip_extraction:
            handler = ArchiveHandler(file_path)
            archive_checksum = hash_md5
            handler.process(lambda path: process_file(path, results, archive_checksum, force_text, skip_extraction))
        result = {
            'file_path': file_path,
            'mime_type': mime_type,
            'size': file_size,
            'hashes': {
                "md5": hash_md5,
                "fuzzy": hash_ssdeep,
                "sha1": hash_sha1,
                "sha256": hash_sha256
            },
            'is_archive': True,
            'words': '',
        }
        results.append(result)
    elif force_text:
        handler_class = get_handler("text/plain")
        if handler_class:
            handler = handler_class(file_path)
            words = handler.extract_words()
            result = {
                'file_path': file_path,
                'mime_type': mime_type,
                'size': file_size,
                'hashes': {
                    "md5": hash_md5,
                    "fuzzy": hash_ssdeep,
                    "sha1": hash_sha1,
                    "sha256": hash_sha256
                },
                'is_archive': False,
                'words': words,
            }
            if archive_checksum:
                result['archive_checksum'] = archive_checksum
            results.append(result)
    else:
        handler_class = get_handler(mime_type if mime_type else "application/octet-stream")
        if handler_class:
            handler = handler_class(file_path)
            if isinstance(handler, ArchiveHandler):
                result = {
                    'file_path': file_path,
                    'mime_type': mime_type,
                    'size': file_size,
                    'hashes': {
                        "md5": hash_md5,
                        "fuzzy": hash_ssdeep,
                        "sha1": hash_sha1,
                        "sha256": hash_sha256
                    },
                    'is_archive': True,
                    'words': '',
                }
                results.append(result)
                archive_checksum = checksum
                handler.process(lambda path: process_file(path, results, archive_checksum, force_text, skip_extraction))
            else:
                words = handler.extract_words()
                if len(words) == 0:
                    logger.info(f"No words returned for MIME type: {mime_type} for file {file_path}")
                result = {
                    'file_path': file_path,
                    'mime_type': mime_type,
                    'size': file_size,
                    'hashes': {
                        "md5": hash_md5,
                        "fuzzy": hash_ssdeep,
                        "sha1": hash_sha1,
                        "sha256": hash_sha256
                    },
                    'is_archive': False,
                    'words': words,
                }
                if archive_checksum:
                    result['archive_checksum'] = archive_checksum
                results.append(result)
        else:
            logger.info(f"No handler registered for MIME type: {mime_type} for file {file_path}")
            return None

if __name__ == '__main__':
    scan()
