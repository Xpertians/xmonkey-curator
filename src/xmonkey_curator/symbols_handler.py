import os
import json
import argparse
import pkg_resources


class TrieNode:
    def __init__(self):
        self.children = {}
        self.isEndOfWord = False
        self.signatures = []


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, symbol, signature):
        node = self.root
        for char in symbol:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.isEndOfWord = True
        node.signatures.append(signature)

    def search(self, text):
        node = self.root
        matches = []
        for char in text:
            if char in node.children:
                node = node.children[char]
                if node.isEndOfWord:
                    matches.extend(node.signatures)
            else:
                node = self.root
        return list(set(matches))


class Signature:
    def __init__(self, package, publisher, license, symbols=None):
        self.package = package
        self.publisher = publisher
        self.license = license
        self.symbols = symbols or []


class SymbolsHandler:
    def __init__(self):
        self.trie = Trie()
        self.signatures = []
        self.load_signatures_from_package()

    def load_signatures_from_package(self):
        resource_package = __name__
        resource_path = '/'.join(('signatures', ''))
        if pkg_resources.resource_isdir(resource_package, resource_path):
            sign_files = pkg_resources.resource_listdir(
                resource_package, resource_path)
            for file_name in sign_files:
                if file_name.endswith('.json'):
                    file_path = pkg_resources.resource_filename(
                        resource_package, f'signatures/{file_name}')
                    with open(file_path, 'r') as file:
                        sign_def = json.load(file)
                        signature = Signature(sign_def['package'],
                                              sign_def['publisher'],
                                              sign_def['license'],
                                              sign_def.get('symbols', []))
                        self.signatures.append(signature)
                        for symbol in signature.symbols:
                            self.trie.insert(symbol, signature)

    def search(self, results):
        matched_results = []
        for entry in results:
            if "words" in entry:
                strings = list(set(entry['words']))
                entry_text = ''.join(strings)
                matched_signatures = self.trie.search(entry_text)
                for signature in matched_signatures:
                    matched_symbols = [
                        symbol
                        for symbol in signature.symbols
                        if symbol in entry_text
                    ]
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
        return matched_results
