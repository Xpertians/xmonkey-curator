import os
import re
import json
import argparse
import pkg_resources
from itertools import combinations
from oslili import LicenseAndCopyrightIdentifier


class License:
    def __init__(
        self, name, include_identifiers,
        exclude_identifiers=None, additional_info=None
    ):
        self.name = name
        self.include_identifiers = include_identifiers
        self.exclude_identifiers = exclude_identifiers or []
        self.additional_info = additional_info or {}

    def matches(self, text):
        text = text.lower()
        inc_all = all(
            re.search(pattern, text, re.IGNORECASE)
            for pattern in self.include_identifiers
        )
        exc_none = not any(
            re.search(pattern, text, re.IGNORECASE)
            for pattern in self.exclude_identifiers
        )
        if inc_all and exc_none:
            return True
        else:
            return False


class LicensesHandler:
    def __init__(self):
        self.licenses = []
        self.load_licenses_from_package()

    def load_licenses_from_package(self):
        resource_package = __name__
        resource_path = '/'.join(('licenses', ''))
        if pkg_resources.resource_isdir(resource_package, resource_path):
            licenses_files = pkg_resources.resource_listdir(
                resource_package, resource_path)
            for file_name in licenses_files:
                if file_name.endswith('.json'):
                    file_path = pkg_resources.resource_filename(
                        resource_package, f'licenses/{file_name}')
                    with open(file_path, 'r') as file:
                        license_def = json.load(file)
                        license = License(
                            license_def['name'],
                            license_def['include_identifiers'],
                            license_def.get('exclude_identifiers', []),
                            license_def.get('additional_info', {})
                        )
                        self.licenses.append(license)

    def execute(self, base_name, results):
        matches = [
            license.name for license in self.licenses
            if license.matches(results)
        ]
        if matches:
            return matches[0]
        else:
            oslili = LicenseAndCopyrightIdentifier()
            spdx_code, license_proba = oslili.identify_license(
                results
            )
            return spdx_code
