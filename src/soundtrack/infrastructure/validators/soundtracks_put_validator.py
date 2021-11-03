import cerberus
from cerberus import Validator

class SoundtracksPutValidator:
    def __init__(self):
        self.__schema = {
            'book': {'type': 'string', 'required': False},
            'soundtrack_title': {'type': 'string', 'required': False},
        }
        self.__validator = Validator()

    def validate(self, new_soundtrack_data: dict):
        return self.__validator.validate(new_soundtrack_data, self.__schema)
