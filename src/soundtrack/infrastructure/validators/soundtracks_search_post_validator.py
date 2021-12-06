import cerberus
from cerberus import Validator

class SoundtracksSearchPostValidator:
    def __init__(self):
        self.__schema = {
            'book': {'type': 'string', 'required': True}
        }
        self.__validator = Validator()

    def validate(self, soundtrack: dict):
        return self.__validator.validate(soundtrack, self.__schema)
