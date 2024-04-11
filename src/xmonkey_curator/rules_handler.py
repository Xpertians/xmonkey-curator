import os
import json
import argparse
import pkg_resources
from itertools import combinations


class Rule:
    def __init__(
        self, identifier, publisher, license, workflow,
        classifier, configuration=None
    ):
        self.identifier = identifier
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
                file_name = os.path.basename(result['file_path']).lower()
                if configStr in file_name:
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
          'FileNameMatch': FileNameMatch,
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
                            rule_def['identifier'],
                            rule_def['publisher'],
                            rule_def['license'],
                            rule_def['workflow'],
                            rule_def['classifier'],
                            rule_def.get('configuration', [])
                        )
                        self.rules.append(rule)

    def execute(self, rule_identifier, results):
        found_rule = None
        for rule in self.rules:
            if rule.identifier == rule_identifier:
                found_rule = rule
                break
        if found_rule is None:
            print(f"Error: Rule '{rule_identifier}' does not exist.")
            exit()

        if 'True' in found_rule.workflow:
            print('Workflow still not implemented')
        else:
            obj = self.classmap[found_rule.classifier](
                found_rule.configuration
            )
            return obj.classifier(results)
