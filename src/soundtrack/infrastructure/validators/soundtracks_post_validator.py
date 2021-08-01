import cerberus
from cerberus import Validator

class SoundtracksPostValidator:
    def __init__(self):
        self.__schema = {
            'soundtrack_id': {'type': 'string', 'required': True},
            'book': {'type': 'string', 'required': True},
            'soundtrack_title': {'type': 'string', 'required': True},
            'author': {'type': 'string', 'required': True}
        }
        self.__validator = Validator()

    def validate(self, soundtrack: dict):
        return self.__validator.validate(soundtrack, self.__schema)
