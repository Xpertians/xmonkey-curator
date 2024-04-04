import os
import json
import argparse
import pkg_resources
from itertools import combinations


class Rule:
    def __init__(self, package, publisher, license, workflow, classifier, configuration=None):
        self.package = package
        self.publisher = publisher
        self.license = license
        self.workflow = workflow
        self.classifier = classifier
        self.configuration = configuration or []

class FileNameMatch:
    def __init__(self, configuration):
        self.results = []
        self.filepaths = []
        self.configuration = configuration

    def substrings(self, word):
        for i, j in combinations(range(len(word) + 1), 2):
            yield word[i : j]

    def classifier(self, results):
        for result in results:
            self.filepaths.append(result['file_path'])
        self.word_set = set().union(*map(self.substrings, self.filepaths))
        for configStr in self.configuration:
            if configStr in self.word_set:
                print(configStr)

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
                        rule = Rule(rule_def['package'], rule_def['publisher'], rule_def['license'], rule_def['workflow'], rule_def['classifier'], rule_def.get('configuration', []))
                        self.rules.append(rule)

    def execute(self, results):
        for rule in self.rules:
            if 'True' in rule.workflow:
                print('workflow still not implemented')
            else:
                obj = self.classmap[rule.classifier](rule.configuration)
                obj.classifier(results)
        return ''
