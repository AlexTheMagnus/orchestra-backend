import cerberus
from cerberus import Validator

class UsersPostValidator:
    def __init__(self):
        self.__schema = {
            'user_id': {'type': 'string', 'required': True},
            'username': {'type': 'string', 'required': True},
            'user_avatar': {'type': 'string', 'required': True}
        }
        self.__validator = Validator()

    def validate(self, user: dict):
        return self.__validator.validate(user, self.__schema)
