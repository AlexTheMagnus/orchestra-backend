from abc import ABC, abstractmethod
from src.soundtrack.domain.soundtrack import Soundtrack
from src.soundtrack.domain.soundtrack_id import SoundtrackId


class SoundtrackRepository(ABC):
    @abstractmethod
    def save(self, soundtrack: Soundtrack):
        pass

    def find(self, soundtrack_id: SoundtrackId) -> Soundtrack:
        pass
