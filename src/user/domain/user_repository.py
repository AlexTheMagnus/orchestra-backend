from abc import ABC, abstractmethod
from typing import List

from ..domain.soundtrack_id import SoundtrackId
from ..domain.user import User
from ..domain.user_id import UserId


class UserRepository(ABC):
    @abstractmethod
    def save(self, user: User):
        pass

    @abstractmethod
    def find(self, user_id: UserId) -> User:
        pass

    @abstractmethod
    def save_favorite(self, user_id: UserId, soundtrack_id: SoundtrackId):
        pass

    @abstractmethod
    def get_favorites(self, user_id: UserId) -> List[SoundtrackId]:
        pass

    @abstractmethod
    def remove_favorite(self, user_id: UserId, soundtrack_id: SoundtrackId):
        pass

    @abstractmethod
    def save_follow(self, follower_id: UserId, followed_id: UserId):
        pass

    @abstractmethod
    def get_followers(self, user_id: UserId) -> List[User]:
        pass

    @abstractmethod
    def get_followed_users(self, user_id: UserId) -> List[User]:
        pass