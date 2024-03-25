import re
import os
from pygments import lex
from pygments.lexers import get_lexer_by_name


class LexerUtilities:
    @staticmethod
    def lexer(lexer_lang, source_code):
        symbols = []
        lexer = get_lexer_by_name(lexer_lang)
        tokens = lex(source_code, lexer)
        for token_type, value in tokens:
            token_type_str = str(token_type)
            keywords = [
                'Class', 'ClassName', 'Function',
                'Def', 'FunctionName', 'Variable',
                'Identifier', 'String', 'Name'
            ]
            if any(keyword in token_type_str for keyword in keywords):
                lower_check_keywords = [
                    'Variable', 'Identifier',
                    'String', 'Name'
                ]
                needs_lower_check = any(
                    kw in token_type_str for kw in lower_check_keywords
                )
                if needs_lower_check and not value[0].islower():
                    continue
                symbols.append(value.lower())
            elif 'PreprocFile' in token_type_str:
                base_name = os.path.basename(value)
                file_name, _ = os.path.splitext(base_name)
                symbols.append(file_name.lower())
        words = list(set(symbols))
        regex = re.compile(r'[^a-zA-Z\s_-]+')
        words = [
            regex.sub('', word).strip() for word in words
            if len(regex.sub('', word).strip()) >= 5
        ]
        return words
