from typing import List

from .user_id import UserId
from .username import Username
from .user_avatar import UserAvatar

class User:

    def __init__(self, user_id: UserId, username: Username, user_avatar: UserAvatar):
        self.__user_id: UserId = user_id
        self.__username: Username = username
        self.__user_avatar: UserAvatar = user_avatar

    @property
    def user_id(self):
        return self.__user_id

    @property
    def username(self):
        return self.__username

    @property
    def user_avatar(self):
        return self.__user_avatar