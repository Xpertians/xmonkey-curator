import sys
import json
import logging
from datetime import datetime
from .file_utilities import FileUtilities
from .__version__ import __version__

logger = logging.getLogger(__name__)


class ReportGenerator:
    def __init__(self, results):
        self.results = results
        self.tool_name = 'xmonkey-curator'
        self.version = __version__
        self.note = ' '.join(sys.argv)
        self.scan_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def generate_report_data(self):
        return {
            'scan_date': self.scan_date,
            'tool_name': self.tool_name,
            'version': self.version,
            'note': self.note,
            'results': self.results,
        }

    def generate_json_report(self, output_file):
        report_data = self.generate_report_data()
        try:
            with open(output_file, 'w') as f:
                json.dump(report_data, f, indent=4)
            logger.info(f"Report successfully generated at {output_file}")
        except Exception as e:
            logger.error(f"Failed to generate report: {e}")

    def save_report(self, filename='report.json'):
        """Saves the report to a file in JSON format, including metadata."""
        report_data = self.generate_report_data()
        with open(filename, 'w') as f:
            json.dump(report_data, f, indent=4)
        print(f"Report saved to {filename}")

    def print_report(self):
        report_data = self.generate_report_data()
        print(json.dumps(report_data, indent=4))


def create_report_entry(file_path, mime_type, checksum, words):
    return {
        'file_path': file_path,
        'mime_type': mime_type,
        'checksum': checksum,
        'extracted_words': words
    }
