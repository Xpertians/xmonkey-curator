import os
import json
import argparse
import pkg_resources
from itertools import combinations


class Rule:
    def __init__(
        self, package, publisher, license, workflow,
        classifier, configuration=None
    ):
        self.package = package
        self.publisher = publisher
        self.license = license
        self.workflow = workflow
        self.classifier = classifier
        self.configuration = configuration or []


class FileNameMatch:
    def __init__(self, configuration):
        self.container = []
        self.filepaths = []
        self.configuration = configuration

    def classifier(self, results):
        for result in results:
            entry = {}
            for configStr in self.configuration:
                configStr = configStr.lower()
                if configStr in result['file_path'].lower():
                    entry['file_path'] = result['file_path']
                    entry['hashes'] = result['hashes']
                    entry['parent_checksum'] = result['parent_checksum']
                    entry['FileNameMatch'] = configStr
                    self.container.append(entry)
        return self.container


class RulesHandler:
    def __init__(self):
        self.rules = []
        self.load_rules_from_package()
        self.classmap = {
          'FileNameMatch': FileNameMatch
        }

    def load_rules_from_package(self):
        resource_package = __name__
        resource_path = '/'.join(('rules', ''))
        if pkg_resources.resource_isdir(resource_package, resource_path):
            sign_files = pkg_resources.resource_listdir(
                resource_package, resource_path)
            for file_name in sign_files:
                if file_name.endswith('.json'):
                    file_path = pkg_resources.resource_filename(
                        resource_package, f'rules/{file_name}')
                    with open(file_path, 'r') as file:
                        rule_def = json.load(file)
                        rule = Rule(
                            rule_def['package'],
                            rule_def['publisher'],
                            rule_def['license'],
                            rule_def['workflow'],
                            rule_def['classifier'],
                            rule_def.get('configuration', [])
                        )
                        self.rules.append(rule)

    def execute(self, results):
        for rule in self.rules:
            if 'True' in rule.workflow:
                print('workflow still not implemented')
            else:
                obj = self.classmap[rule.classifier](rule.configuration)
                return obj.classifier(results)
