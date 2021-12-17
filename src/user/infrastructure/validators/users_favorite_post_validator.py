import cerberus
from cerberus import Validator

class UsersFavoritePostValidator:
    def __init__(self):
        self.__schema = {
            'user_id': {'type': 'string', 'required': True},
            'soundtrack_id': {'type': 'string', 'required': True}
        }
        self.__validator = Validator()

    def validate(self, favorite: dict):
        return self.__validator.validate(favorite, self.__schema)
