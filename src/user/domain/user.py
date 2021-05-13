from .user_id import UserId
from .soundtrack_id import SoundtrackId


class User:

    def __init__(self, user_id: UserId, favorites: list[SoundtrackId], likes: list[SoundtrackId]):
        self.__user_id: UserId = user_id
        self.__favorites: list[SoundtrackId] = favorites
        self.__likes: list[SoundtrackId] = likes

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
