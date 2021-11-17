from abc import ABC, abstractmethod
from typing import List

from ..domain.soundtrack_id import SoundtrackId
from ..domain.user import User
from ..domain.user_id import UserId


class UserRepository(ABC):
    @abstractmethod
    def save(self, user: User):
        pass

    def find(self, user_id: UserId) -> User:
        pass

    def get_favorites(self, user_id: UserId) -> List[SoundtrackId]:
        pass

    def save_favorite(self, user_id: UserId, soundtrack_id: SoundtrackId):
        pass