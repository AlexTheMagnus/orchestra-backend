class UserId():

    def __init__(self, user_id: str):
        self.__value: str = user_id

    @staticmethod
    def from_string(user_id: str):
        return UserId(user_id)

    @property
    def value(self):
        return self.__value
