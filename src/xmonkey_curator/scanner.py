import os
import click
import logging
import mimetypes
from tqdm import tqdm
from xmonkey_curator.handler_registry import get_handler
from xmonkey_curator.report_generator import ReportGenerator
from xmonkey_curator.handlers.archive_handler import ArchiveHandler
from xmonkey_curator.file_utilities import FileUtilities
from xmonkey_curator.symbols_handler import SymbolsHandler
from xmonkey_curator.rules_handler import RulesHandler
from xmonkey_curator.signatures_handler import SignatureUpdater


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
    'inode/'
]

EXCLUDED_MIME_TYPES = [
    'application/pgp-signature',
    'application/x-font-type1',
    'application/pdf',
    'application/x-git',
    'application/pkix-attr-cert',
    'application/msword'
]

ARCHIVE_MIME_TYPES = [
    'application/zip',
    'application/gzip',
    'application/x-tar',
    'application/x-rpm',
    'application/x-debian-package',
    'application/java-archive',
    'application/vnd.android.package-archive',
]


@click.group()
def cli():
    pass


@cli.command(help="Scan target files using selected options")
@click.argument('path', type=click.Path(exists=True))
@click.option('--force-text', '-t', is_flag=True,
              help="Force using StringExtract for all files.")
@click.option('--recursive-extraction', '-r', is_flag=True,
              help="Extracting archives files.")
@click.option('--export-symbols', '-s', is_flag=True,
              help="Include words in the final report.")
@click.option('--match-symbols', '-m', is_flag=True,
              help="Match symbols against signatures.")
@click.option('--print-report', '-p', is_flag=True,
              help="Print the report to screen.")
def scan(path,
         force_text,
         recursive_extraction,
         export_symbols,
         match_symbols,
         print_report):
    if not recursive_extraction:
        export_symbols = False
    if not export_symbols:
        match_symbols = False
    results = []
    report = {}
    if os.path.isdir(path):
        logger.info(f"Scanning directory: {path}")
        all_files = [
            os.path.join(root, file)
            for root, _, files in os.walk(path)
            for file in files
        ]
        for file_path in tqdm(all_files, desc="Scanning files"):
            result = process_file(file_path, results, '',
                                  force_text, recursive_extraction,
                                  export_symbols)
            if result:
                results.append(result)
    else:
        logger.info(f"Scanning file: {path}")
        result = process_file(
            path,
            results,
            '',
            force_text,
            recursive_extraction,
            export_symbols
        )
        if result:
            results.append(result)
    report['scan_results'] = results
    rules = RulesHandler()
    ruleset_results = rules.execute(results)
    if ruleset_results:
        report['ruleset_results'] = ruleset_results
    if match_symbols:
        sym_matcher = SymbolsHandler()
        matches = sym_matcher.search(results)
        report['symbols_matching'] = matches
    report_generator = ReportGenerator(report)
    if print_report:
        report_generator.print_report()
    else:
        report_generator.save_report('scan_report.json')


@cli.command(name='update', help="Update local signature files")
def update_signatures_command():
    SignatureUpdater.fetch_and_update_signatures(
        'Xpertians', 'BSA-Signatures-Experimental', 'signatures'
    )
    click.echo("Signatures updated successfully.")


def process_file(file_path,
                 results,
                 archive_checksum=None,
                 force_text=False,
                 recursive_extraction=False,
                 export_symbols=False):
    mime_type = FileUtilities.identify_mime_type(file_path)
    file_size = FileUtilities.get_file_size(file_path)
    hash_md5, hash_sha1, hash_sha256, hash_ssdeep = (
            FileUtilities.calculate_hashes(file_path)
        )
    if mime_type in EXCLUDED_MIME_TYPES:
        logger.info(
                    f"Skipping {file_path} as MIME: {mime_type} is excluded"
                )
        return None
    elif any(mime_type.startswith(prefix)
             for prefix in EXCLUDED_MIME_TYPE_PREFIXES):
        logger.info(
                    f"Skipping {file_path} as CLASS: {mime_type} is excluded"
                )
        return None
    elif mime_type in ARCHIVE_MIME_TYPES:
        if recursive_extraction:
            handler = ArchiveHandler(file_path)
            archive_checksum = hash_md5
            handler.process(
                lambda path: process_file(
                    path,
                    results,
                    archive_checksum,
                    force_text,
                    recursive_extraction,
                    export_symbols
                )
            )
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
        }
        if export_symbols:
            result['words'] = ''
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
            }
            if export_symbols:
                result['words'] = handler.extract_words()
            if archive_checksum:
                result['parent_checksum'] = archive_checksum
            results.append(result)
    else:
        handler_class = get_handler(
            mime_type if mime_type else "application/octet-stream"
        )
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
                }
                if export_symbols:
                    result['words'] = ''
                results.append(result)
                archive_checksum = checksum
                handler.process(
                    lambda path: process_file(
                        path,
                        results,
                        archive_checksum,
                        force_text,
                        recursive_extraction,
                        export_symbols
                    )
                )
            else:
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
                }
                if export_symbols:
                    words = handler.extract_words()
                    if len(words) == 0:
                        logger.info(
                            f"No words returned for MIME type: {mime_type} "
                            f"for file {file_path}"
                        )
                    result['words'] = words
                if archive_checksum:
                    result['parent_checksum'] = archive_checksum
                results.append(result)
        else:
            logger.info(
                f"No handler registered for MIME type: {mime_type} "
                f"for file {file_path}"
            )
            return None


if __name__ == '__main__':
    cli()
