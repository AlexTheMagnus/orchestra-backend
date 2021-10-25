from abc import ABC, abstractmethod
from typing import List

from .soundtrack import Soundtrack
from .soundtrack_id import SoundtrackId
from .user_id import UserId


class SoundtrackRepository(ABC):
    @abstractmethod
    def save(self, soundtrack: Soundtrack):
        pass

    def find(self, soundtrack_id: SoundtrackId) -> Soundtrack:
        pass

    def find_by_author(self, author: UserId) -> List[Soundtrack]:
        pass

    def update(self, soundtrack: Soundtrack):
        pass