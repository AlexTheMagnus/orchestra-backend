from abc import ABC, abstractmethod
from typing import List, Optional

from .soundtrack import Soundtrack
from .soundtrack_id import SoundtrackId
from .user_id import UserId


class SoundtrackRepository(ABC):
    @abstractmethod
    def save(self, soundtrack: Soundtrack):
        pass

    def find(self, soundtrack_id: SoundtrackId) -> Optional[Soundtrack]:
        pass

    def find_by_author(self, author: UserId) -> List[Soundtrack]:
        pass

    def update(self, soundtrack: Soundtrack):
        pass

    def delete(self, soundtrack_id: SoundtrackId):
        pass

    def save_like(self, user_id: UserId, soundtrack_id: SoundtrackId):
        pass

    def get_likes(self, soundtrack_id: SoundtrackId) -> List[UserId]:
        pass

    def delete_like(self, user_id: UserId, soundtrack_id: SoundtrackId):
        pass