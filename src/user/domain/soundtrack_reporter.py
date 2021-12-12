from abc import ABC, abstractmethod

from ..domain.soundtrack_id import SoundtrackId


class SoundtrackReporter(ABC):
    @abstractmethod
    def exist(self, soundtrack_id: SoundtrackId) -> bool:
        pass