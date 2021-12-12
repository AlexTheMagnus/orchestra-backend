from abc import ABC, abstractmethod
from typing import List, Optional

from .search_options import SearchOptions
from .soundtrack import Soundtrack
from .soundtrack_id import SoundtrackId
from .user_id import UserId

class SoundtrackRepository(ABC):
    @abstractmethod
    def save(self, soundtrack: Soundtrack):
        pass

    @abstractmethod
    def find(self, soundtrack_id: SoundtrackId) -> Optional[Soundtrack]:
        pass

    @abstractmethod
    def find_by_author(self, author: UserId) -> List[Soundtrack]:
        pass

    @abstractmethod
    def search(self, search_options: SearchOptions) -> List[Soundtrack]:
        pass

    @abstractmethod
    def update(self, soundtrack: Soundtrack):
        pass

    @abstractmethod
    def delete(self, soundtrack_id: SoundtrackId):
        pass

    @abstractmethod
    def save_like(self, user_id: UserId, soundtrack_id: SoundtrackId):
        pass

    @abstractmethod
    def get_likes(self, soundtrack_id: SoundtrackId) -> List[UserId]:
        pass

    @abstractmethod
    def delete_like(self, user_id: UserId, soundtrack_id: SoundtrackId):
        pass