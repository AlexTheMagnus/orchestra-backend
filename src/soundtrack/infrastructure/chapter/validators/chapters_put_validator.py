import cerberus
from cerberus import Validator

class ChaptersPutValidator:
    def __init__(self):
        self.__schema = {
            'chapter_number': {'type': 'integer', 'required': False},
            'theme': {'type': 'string', 'required': False},
            'chapter_title': {'type': 'string', 'required': False}
        }
        self.__validator = Validator()

    def validate(self, new_chapter_data: dict):
        return self.__validator.validate(new_chapter_data, self.__schema)
