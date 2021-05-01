class Username():

    def __init__(self, username: str):
        self.__value: str = username

    @staticmethod
    def from_string(str_username: str):
        return Username(str_username)

    @property
    def value(self):
        return self.__value
