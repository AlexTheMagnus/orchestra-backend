from .user_id import UserId
from .email import Email
from .username import Username
from .avatar import Avatar


class User:

    def __init__(self, user_id: UserId, email: Email, username: Username, avatar: Avatar):
        self.__user_id: UserId = user_id
        self.__email: Email = email
        self.__username: Username = username
        self.__avatar: Avatar = avatar

    @property
    def user_id(self):
        return self.__user_id

    @property
    def email(self):
        return self.__email

    @property
    def username(self):
        return self.__username

    @property
    def avatar(self):
        return self.__avatar

    def get_id(self):
        return self.__user_id
