import cerberus
from cerberus import Validator
from typing import List

List_type = cerberus.TypeDefinition('List', (List,), ())

Validator.types_mapping['List'] = List_type


class SoundtracksPostValidator:
    def __init__(self):
        self.__schema = {
            'soundtrack_id': {'type': 'string', 'required': True},
            'book': {'type': 'string', 'required': True},
            'soundtrack_title': {'type': 'string', 'required': True},
            'author': {'type': 'string', 'required': True},
            'chapters': {'type': 'List', 'required': True, 'nullable': True}

        }
        self.__validator = Validator()

    def validate(self, soundtrack: dict):
        return self.__validator.validate(soundtrack, self.__schema)
