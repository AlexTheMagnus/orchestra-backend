import cerberus
from cerberus import Validator

class ChaptersPostValidator:
    def __init__(self):
        self.__schema = {
            'chapter_id': {'type': 'string', 'required': True},
            'soundtrack_id': {'type': 'string', 'required': True},
            'chapter_number': {'type': 'integer', 'required': True},
            'theme': {'type': 'string', 'required': True},
            'chapter_title': {'type': 'string', 'required': True}
        }
        self.__validator = Validator()

    def validate(self, chapter: dict):
        return self.__validator.validate(chapter, self.__schema)
