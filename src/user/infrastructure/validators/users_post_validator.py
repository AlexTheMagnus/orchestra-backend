import cerberus
from cerberus import Validator

class UsersPostValidator:
    def __init__(self):
        self.__schema = {
            'access_code': {'type': 'string', 'required': True}
        }
        self.__validator = Validator()

    def validate(self, user: dict):
        return self.__validator.validate(user, self.__schema)
