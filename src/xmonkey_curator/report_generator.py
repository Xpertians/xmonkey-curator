import sys
import json
import logging
from tabulate import tabulate
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
        data = self.generate_report_data()
        summary_data = {
            "Scan Date": data["scan_date"],
            "Tool Name": data["tool_name"],
            "Version": data["version"],
            "Files Scanned": len(data["results"]["scan_results"])
        }
        summary_table = tabulate(
            [summary_data.values()],
            headers=summary_data.keys(),
            tablefmt="grid"
        )
        detailed_results = []
        for result in data["results"]["scan_results"]:
            detailed_results.append([
                result["file_path"],
                result["mime_type"],
                result["size"]
            ])
        detailed_table = tabulate(
            detailed_results,
            headers=["File Path", "MIME Type", "Size"],
            tablefmt="grid"
        )
        signature_summary = {}
        if "symbols_matching" in data["results"]:
            for symbol in data["results"]["symbols_matching"]:
                signature = (
                    f"{symbol['signature_properties']['package']} - "
                    f"{symbol['signature_properties']['publisher']}"
                )
                license = symbol['signature_properties']['license']
                symbol_count = len(symbol["matched_symbols"])
                if signature not in signature_summary:
                    signature_summary[signature] = {
                        "license": license,
                        "file_count": 0,
                        "total_symbols": 0
                    }
                signature_summary[signature]["file_count"] += 1
                signature_summary[signature]["total_symbols"] += symbol_count
        signature_data = [
            [
                sig,
                details["license"],
                details["file_count"],
                details["total_symbols"]
            ]
            for sig, details in signature_summary.items()
        ]
        signature_table = tabulate(
            signature_data,
            headers=["Signature", "License", "Files Found", "Total Symbols"],
            tablefmt="grid"
        )
        print("Summary Information:")
        print(summary_table)
        print("\nDetailed Scan Results:")
        print(detailed_table)
        if "symbols_matching" in data["results"]:
            print("\nSignature Matches:")
            print(signature_table)


def create_report_entry(file_path, mime_type, checksum, words):
    return {
        'file_path': file_path,
        'mime_type': mime_type,
        'checksum': checksum,
        'extracted_words': words
    }
