import json
import logging
from .file_utilities import FileUtilities

logger = logging.getLogger(__name__)


class ReportGenerator:
    def __init__(self, results):
        self.results = results

    def generate_json_report(self, output_file):
        try:
            with open(output_file, 'w') as f:
                json.dump(self.results, f, indent=4)
            logger.info(f"Report successfully generated at {output_file}")
        except Exception as e:
            logger.error(f"Failed to generate report: {e}")

    def print_report(self):
        """Prints the report to the console."""
        for result in self.results:
            print(json.dumps(result, indent=4))

    def save_report(self, filename='report.json'):
        """Saves the report to a file in JSON format."""
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=4)
        print(f"Report saved to {filename}")


def create_report_entry(file_path, mime_type, checksum, words):
    return {
        'file_path': file_path,
        'mime_type': mime_type,
        'checksum': checksum,
        'extracted_words': words
    }
