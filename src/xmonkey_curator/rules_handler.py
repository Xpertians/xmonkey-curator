import os
import json
import argparse
import pkg_resources


class Rule:
    def __init__(self, package, publisher, license, worflow, symbols=None):
        self.package = package
        self.publisher = publisher
        self.license = license
        self.worflow = worflow
        self.symbols = symbols or []


class RulesHandler:
    def __init__(self):
        self.rules = []
        self.load_rules_from_package()

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
                        rule = Rule(rule_def['package'],
                                              rule_def['publisher'],
                                              rule_def['worflow'],
                                              rule_def['license'],
                                              rule_def.get('symbols', []))
                        self.rules.append(rule)
                        for symbol in rule.symbols:
                            #here is the action
                            print(symbol, signature)

    def execute(self, results):
        print(results)
        return ''
