import logging
import re
from ..base_handler import BaseFileHandler
from pygments import lex
from pygments.lexers import get_lexer_by_name


class RustFileHandler(BaseFileHandler):
    def __init__(self, file_path):
        """
        Initializes the handler with a specific file path.
        """
        super().__init__(file_path)
        self.logger = logging.getLogger(__name__)
        self.file_path = file_path

    def extract_words(self):
        symbols = []
        lexer = get_lexer_by_name('rust')
        try:
            with open(self.file_path, 'r') as file:
                source_code = file.read()
                tokens = lex(source_code, lexer)
                for token_type, value in tokens:
                    token_type_str = str(token_type)
                    if 'Class' in token_type_str or 'ClassName' in token_type_str:
                        symbols.append(value.lower())
                    elif 'Function' in token_type_str or 'Def' in token_type_str or 'FunctionName' in token_type_str:
                        symbols.append(value.lower())
                    elif 'Variable' in token_type_str or 'Identifier' in token_type_str:
                        if value[0].islower():
                            symbols.append(value.lower())
                    elif 'String' in token_type_str or 'Name' in token_type_str:
                        if value[0].islower():
                            symbols.append(value.lower())
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except Exception as e:
            print(f"Error processing file: {e}")
        words = list(set(symbols))
        regex = re.compile(r'[^a-zA-Z\s_-]+')
        words = [regex.sub('', word).strip() for word in words if len(regex.sub('', word).strip()) >= 5]
        return words