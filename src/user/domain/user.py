from typing import List

from .user_id import UserId
from .soundtrack_id import SoundtrackId


class User:

    def __init__(self, user_id: UserId, favorites: List[SoundtrackId], likes: List[SoundtrackId]):
        self.__user_id: UserId = user_id
        self.__favorites: List[SoundtrackId] = favorites
        self.__likes: List[SoundtrackId] = likes

    @property
    def user_id(self):
        return self.__user_id

    @property
    def favorites(self):
        return self.__favorites

    @property
    def likes(self):
        return self.__likes

    def get_id(self):
        return self.__user_id
