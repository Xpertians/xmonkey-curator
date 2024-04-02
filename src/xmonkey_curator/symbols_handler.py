import re
import os
import json
import argparse
import pkg_resources


class Signature:
    def __init__(self, package, publisher, license, symbols=None):
        self.package = package
        self.publisher = publisher
        self.license = license
        self.symbols = symbols or []


class SymbolsHandler:

    def __init__(self):
        self.signatures = []
        self.load_signatures_from_package()

    def load_signatures_from_package(self):
        resource_package = __name__
        resource_path = '/'.join(('signatures', ''))
        if pkg_resources.resource_isdir(resource_package, resource_path):
            sign_files = pkg_resources.resource_listdir(resource_package, resource_path)
            for file_name in sign_files:
                if file_name.endswith('.json'):
                    file_path = pkg_resources.resource_filename(resource_package, f'signatures/{file_name}')
                    with open(file_path, 'r') as file:
                        sign_def = json.load(file)
                        self.signatures.append(Signature(sign_def['package'],
                                               sign_def['publisher'],
                                               sign_def['license'],
                                               sign_def.get('symbols', [])))

    def search(self, results):
        matched_results = []
        for entry in results:
            if "words" in entry:
                strings = list(set(entry['words']))
                entry_text = ''.join(strings)
                for signature in self.signatures:
                    matched_symbols = [pattern for pattern in signature.symbols if re.search(pattern, entry_text, re.IGNORECASE)]
                    if matched_symbols:
                        matched_info = {
                            'file_path': entry['file_path'],
                            'signature_properties': {
                                'package': signature.package,
                                'publisher': signature.publisher,
                                'license': signature.license
                            },
                            'matched_symbols': matched_symbols
                        }
                        matched_results.append(matched_info)
        print(matched_results)
        return matched_results


