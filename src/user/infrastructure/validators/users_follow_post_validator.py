import cerberus
from cerberus import Validator

class UsersFollowPostValidator:
    def __init__(self):
        self.__schema = {
            'follower_id': {'type': 'string', 'required': True},
            'followed_id': {'type': 'string', 'required': True},
        }
        self.__validator = Validator()

    def validate(self, follow: dict):
        return self.__validator.validate(follow, self.__schema)
