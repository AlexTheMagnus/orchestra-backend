from .exceptions.not_a_valid_username_error import NotAValidUsernameError

class Username():

    def __init__(self, username: str):
        username = username.strip()
        self.__validate_not_an_empty_string(username)
        self.__value: str = username

    @staticmethod
    def from_string(username: str):
        return Username(username)

    @property
    def value(self):
        return self.__value

    def __validate_not_an_empty_string(self, username: str):
        if username == "":
            raise(NotAValidUsernameError(username))
