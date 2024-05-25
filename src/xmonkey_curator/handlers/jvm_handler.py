import re
import os
import logging
from ..base_handler import BaseFileHandler
from ..lexer_utilities import LexerUtilities
from pygments import lex
from pygments.lexers import get_lexer_by_name
from enum import Enum
from io import BytesIO
from pathlib import Path
from pprint import pprint
import typer
import re


class JvmFileHandler(BaseFileHandler):
    class Constants(Enum):
        CONSTANT_Class              = 7
        CONSTANT_Fieldref           = 9
        CONSTANT_Methodref          = 10
        CONSTANT_InterfaceMethodref = 11
        CONSTANT_String             = 8
        CONSTANT_Integer            = 3
        CONSTANT_Float              = 4
        CONSTANT_Long               = 5
        CONSTANT_Double             = 6
        CONSTANT_NameAndType        = 12
        CONSTANT_Utf8               = 1
        CONSTANT_MethodHandle       = 15
        CONSTANT_MethodType         = 16
        CONSTANT_InvokeDynamic      = 18


    ACCESS_FLAGS = {
        "class":  [
            ("ACC_PUBLIC"       ,0x0001),
            ("ACC_FINAL"        ,0x0010),
            ("ACC_SUPER"        ,0x0020),
            ("ACC_INTERFACE"    ,0x0200),
            ("ACC_ABSTRACT"     ,0x0400),
            ("ACC_SYNTHETIC"    ,0x1000),
            ("ACC_ANNOTATION"   ,0x2000),
            ("ACC_ENUM"         ,0x4000),
        ],
        "field": [
            ("ACC_PUBLIC"       ,0x0001),
            ("ACC_PRIVATE"      ,0x0002),
            ("ACC_PROTECTED"    ,0x0004),
            ("ACC_STATIC"       ,0x0008),
            ("ACC_FINAL"        ,0x0010),
            ("ACC_VOLATILE"     ,0x0040),
            ("ACC_TRANSIENT"    ,0x0080),
            ("ACC_SYNTHETIC"    ,0x1000),
            ("ACC_ENUM"         ,0x4000),
        ],
        "method": [
            ("ACC_PUBLIC"       ,0x0001),
            ("ACC_PRIVATE"      ,0x0002),
            ("ACC_PROTECTED"    ,0x0004),
            ("ACC_STATIC"       ,0x0008),
            ("ACC_FINAL"        ,0x0010),
            ("ACC_SYNCHRONIZED" ,0x0020),
            ("ACC_BRIDGE"       ,0x0040),
            ("ACC_VARARGS"      ,0x0080),
            ("ACC_NATIVE"       ,0x0100),
            ("ACC_ABSTRACT"     ,0x0400),
            ("ACC_STRICT"       ,0x0800),
            ("ACC_SYNTHETIC"    ,0x1000),
        ],
    }

    def __init__(self, file_path):
        """
        Initializes the handler with a specific file path.
        """
        super().__init__(file_path)
        self.logger = logging.getLogger(__name__)
        self.file_path = file_path
        self.constant_pool = []

    def extract_words(self):
        symbols = []
        base_name = os.path.basename(self.file_path)
        file_name = os.path.splitext(base_name)[0]
        symbols.append(file_name.lower())
        
        unique_strings = set()
        with open(self.file_path, mode="rb") as f:
            class_file = self.parse_class_file(BytesIO(f.read()))
            for entry in class_file['constant_pool']:
                if 'bytes' in entry:
                    string_data = entry['bytes'].decode('utf-8').strip()
                    cleaned_data = re.sub(r'[^a-zA-Z0-9/.\s]', '', string_data)
                    if cleaned_data and len(cleaned_data) >= 4:
                        unique_strings.add(cleaned_data)
        unique_strings_list = list(unique_strings)
        if unique_strings_list:
            symbols.extend(unique_strings_list)

        words = LexerUtilities.clean_strings(symbols)
        return words

    def parse_ux(self, file: BytesIO, length: int) -> int:
        return int.from_bytes(file.read(length), "big")


    def parse_u1(self, file: BytesIO) -> int:
        return self.parse_ux(file, 1)


    def parse_u2(self, file: BytesIO) -> int:
        return self.parse_ux(file, 2)


    def parse_u4(self, file: BytesIO) -> int:
        return self.parse_ux(file, 4)


    def parse_constant_pool(self, f: BytesIO, pool_size: int) -> int:
        constant_pool = []
        for _ in range(pool_size):
            cp_info = {}
            tag = self.parse_u1(f)
            constant = self.Constants(tag)

            if constant in (
                self.Constants.CONSTANT_Methodref,
                self.Constants.CONSTANT_InterfaceMethodref,
                self.Constants.CONSTANT_Fieldref,
            ):
                cp_info["tag"] = constant.value
                cp_info["class_index"] = self.parse_u2(f)
                cp_info["name_and_type_index"] = self.parse_u2(f)
            elif constant in (self.Constants.CONSTANT_Class, self.Constants.CONSTANT_String):
                cp_info["tag"] = constant.value
                cp_info["name_index"] = self.parse_u2(f)
            elif constant == self.Constants.CONSTANT_Utf8:
                cp_info["tag"] = constant.value
                cp_info["length"] = self.parse_u2(f)
                cp_info["bytes"] = f.read(cp_info["length"])
            elif constant == self.Constants.CONSTANT_NameAndType:
                cp_info["tag"] = constant.value
                cp_info["name_index"] = self.parse_u2(f)
                cp_info["descriptor_index"] = self.parse_u2(f)
            elif constant in (self.Constants.CONSTANT_Integer, self.Constants.CONSTANT_Float):
                cp_info["tag"] = constant.value
                cp_info["bytes"] = f.read(4)
            elif constant in (self.Constants.CONSTANT_Long, self.Constants.CONSTANT_Double):
                cp_info["tag"] = constant.value
                cp_info["high_bytes"] = f.read(4)
                cp_info["low_bytes"] = f.read(4)
            elif constant == self.Constants.CONSTANT_MethodHandle:
                cp_info["tag"] = constant.value
                cp_info["reference_kind"] = self.parse_u1(f)
                cp_info["reference_index"] = self.parse_u2(f)
            elif constant == self.Constants.CONSTANT_MethodType:
                cp_info["tag"] = constant.value
                cp_info["descriptor_index"] = self.parse_u2(f)
            elif constant == self.Constants.CONSTANT_InvokeDynamic:
                cp_info["tag"] = constant.value
                cp_info["bootstrap_method_attr_index"] = self.parse_u2(f)
                cp_info["name_and_type_index"] = self.parse_u2(f)
            else:
                assert False, f"Unexpected tag encountered {tag = }"
            constant_pool.append(cp_info)
        return constant_pool


    def parse_access_flags(self, val: int, flags: [(str, int)]) -> list[str]:
        return [name for (name, mask) in flags if not (val & mask)]


    def parse_attributes(self, f: BytesIO, attributes_count: int) -> list:
        attributes = []

        for _ in range(attributes_count):
            attribute_info = {}
            attribute_info["attribute_name_index"] = self.parse_u2(f)
            attribute_info["attribute_length"] = self.parse_u4(f)
            attribute_info["info"] = f.read(attribute_info["attribute_length"])
            attributes.append(attribute_info)

        return attributes


    def parse_methods(self, f: BytesIO, methods_count: int) -> list:
        methods = []

        for _ in range(methods_count):
            method_info = {}
            method_info["access_flags"] = self.parse_access_flags(
                self.parse_u2(f), ACCESS_FLAGS["method"]
            )
            method_info["name_index"] = self.parse_u2(f)
            method_info["descriptor_index"] = self.parse_u2(f)
            method_info["attributes_count"] = self.parse_u2(f)
            method_info["attributes"] = self.parse_attributes(f, method_info["attributes_count"])
            methods.append(method_info)
        return methods


    def parse_fields(self, f: BytesIO, fields_count: int) -> dict:
        fields = []

        for _ in range(fields_count):
            field_info = {}
            field_info["access_flags"] = self.parse_access_flags(
                self.parse_u2(f), self.ACCESS_FLAGS["field"]
            )
            field_info["name_index"] = self.parse_u2(f)
            field_info["descriptor_index"] = self.parse_u2(f)
            field_info["attributes_count"] = self.parse_u2(f)
            field_info["attributes"] = self.parse_attributes(f, field_info["attributes_count"])
            fields.append(field_info)

        return fields


    def parse_interfaces(self, f: BytesIO, interfaces_count: int) -> dict:
        interfaces = []
        for _ in range(interfaces_count):
            self.parse_u1(f)  # Discard tag
            class_info = {"tag": "CONSTANT_Class", "name_index": self.parse_u2(f)}
            interfaces.append(class_info)
        return interfaces


    def parse_class_file(self, f: BytesIO) -> dict:
        class_file = {}
        class_file["magic"] = str(hex(self.parse_u4(f))).upper()
        class_file["minor"] = self.parse_u2(f)
        class_file["major"] = self.parse_u2(f)
        class_file["constant_pool_count"] = self.parse_u2(f)
        class_file["constant_pool"] = self.parse_constant_pool(
            f, class_file["constant_pool_count"] - 1
        )
        class_file["access_flags"] = self.parse_access_flags(self.parse_u2(f), self.ACCESS_FLAGS["class"])
        class_file["this_class"] = self.parse_u2(f)
        class_file["super_class"] = self.parse_u2(f)
        class_file["interfaces_count"] = self.parse_u2(f)
        class_file["interfaces"] = self.parse_interfaces(f, class_file["interfaces_count"])
        class_file["fields_count"] = self.parse_u2(f)
        class_file["fields"] = self.parse_fields(f, class_file["fields_count"])
        class_file["methods_count"] = self.parse_u2(f)
        class_file["methods"] = self.parse_methods(f, class_file["methods_count"])
        class_file["attributes_count"] = self.parse_u2(f)
        class_file["attributes"] = self.parse_attributes(f, class_file["attributes_count"])

        return class_file
