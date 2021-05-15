from typing import List

from .user_id import UserId
from .soundtrack_id import SoundtrackId


class User:

    def __init__(
        self, user_id: UserId,
        favorites: List[SoundtrackId],
        likes: List[SoundtrackId],
        soundtracks: List[SoundtrackId],
        following: List[UserId],
        followers: List[UserId]
    ):
        self.__user_id: UserId = user_id
        self.__favorites: List[SoundtrackId] = favorites
        self.__likes: List[SoundtrackId] = likes
        self.__soundtracks: List[SoundtrackId] = soundtracks
        self.__following: List[UserId] = following
        self.__followers: List[UserId] = followers

    @property
    def user_id(self):
        return self.__user_id

    @property
    def favorites(self):
        return self.__favorites

    @property
    def likes(self):
        return self.__likes

    @property
    def soundtracks(self):
        return self.__soundtracks

    @property
    def followers(self):
        return self.__followers

    @property
    def following(self):
        return self.__following

    def get_id(self):
        return self.__user_id
