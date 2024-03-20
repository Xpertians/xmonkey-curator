import json
import logging
from .file_utilities import FileUtilities  # Assuming this class provides MIME type and checksum functionalities.

logger = logging.getLogger(__name__)

class ReportGenerator:
    def __init__(self, results):
        """
        Initializes the report generator with the scanning results.
        :param results: A list of dictionaries, each containing the scanning result for a single file.
        """
        self.results = results

    def generate_json_report(self, output_file):
        """
        Generates a JSON report from the scanning results.
        :param output_file: Path to the output file where the JSON report will be saved.
        """
        try:
            with open(output_file, 'w') as f:
                json.dump(self.results, f, indent=4)
            logger.info(f"Report successfully generated at {output_file}")
        except Exception as e:
            logger.error(f"Failed to generate report: {e}")

def create_report_entry(file_path, mime_type, checksum, words):
    """
    Creates a single report entry for a file.
    :param file_path: Path to the file.
    :param mime_type: MIME type of the file.
    :param checksum: MD5 checksum of the file.
    :param words: List of extracted words from the file.
    :return: A dictionary representing the report entry.
    """
    return {
        'file_path': file_path,
        'mime_type': mime_type,
        'checksum': checksum,
        'extracted_words': words
    }

# Example usage
if __name__ == '__main__':
    # Assuming we have a list of file paths to process and this is a simplified example
    file_paths = ['/path/to/file1.txt', '/path/to/file2.txt']
    results = []

    for file_path in file_paths:
        mime_type = FileUtilities.identify_mime_type(file_path)
        checksum = FileUtilities.calculate_checksum(file_path)
        # Assuming a function 'extract_words' returns a list of words from the file
        words = FileUtilities.extract_words(file_path)
        results.append(create_report_entry(file_path, mime_type, checksum, words))

    # Generate the report
    report_generator = ReportGenerator(results)
    report_generator.generate_json_report('scan_report.json')
