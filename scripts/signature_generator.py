import json
from tqdm import tqdm
from datetime import datetime


def create_superstring_from_json(json_path):
    superstring = ""
    with open(json_path, 'r') as file:
        data_json = json.load(file)
        total_results = len(data_json['results']['scan_results'])
        for result in tqdm(
                data_json['results']['scan_results'],
                desc="Creating superstring", total=total_results
                ):
            for word in result['words']:
                superstring += word + " "
    return superstring


def find_common_symbols(source_json_path, superstring):
    common_symbols = set()
    with open(source_json_path, 'r') as file:
        data_json = json.load(file)
        total_results = len(data_json['results']['scan_results'])
        for result in tqdm(
                data_json['results']['scan_results'],
                desc="Finding common symbols", total=total_results
                ):
            words = list(set(result['words']))
            for word in words:
                split_words = word.split()
                for split_word in split_words:
                    if len(split_word) > 15:
                        continue
                    if len(split_word) < 5:
                        continue
                    if split_word in superstring:
                        common_symbols.add(split_word)
    return common_symbols


def save_to_json(common_symbols, output_path='signature.json'):
    today_date = datetime.now().strftime("%Y-%m-%d")
    data_to_save = {
        "publisher": "<PUBLISHER>",
        "updated": today_date,
        "package": "<PACKAGE_NAME>",
        "license": "<LICENSE>",
        "symbols": list(common_symbols)
    }
    with open(output_path, 'w') as json_file:
        json.dump(data_to_save, json_file, indent=4)


def main(source_code_json_path, binary_json_path):
    binary_superstring = create_superstring_from_json(binary_json_path)
    common_symbols = find_common_symbols(
        source_code_json_path, binary_superstring
    )
    print(f'Common Symbols: {common_symbols}')
    print(f'Total common symbols: {len(common_symbols)}')
    save_to_json(common_symbols)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description='Find common symbols between source code and binary.'
    )
    parser.add_argument(
        'source_code_json_path',
        type=str,
        help='Path to the JSON file with source code symbols'
    )
    parser.add_argument(
        'binary_json_path',
        type=str,
        help='Path to the JSON file with binary symbols'
    )
    args = parser.parse_args()
    main(args.source_code_json_path, args.binary_json_path)
