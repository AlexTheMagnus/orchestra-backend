import cerberus
from cerberus import Validator

class SoundtracksUserGetValidator():
    def __init__(self):
        self.__schema = {
            'author': {'type': 'string', 'required': True}
        }
        self.__validator = Validator()

    def validate(self, author: dict):
        return self.__validator.validate(author, self.__schema)
