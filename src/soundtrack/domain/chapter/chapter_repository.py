from abc import ABC, abstractmethod
from typing import List

from .chapter import Chapter
from .chapter_id import ChapterId
from ..soundtrack_id import SoundtrackId


class ChapterRepository(ABC):
    @abstractmethod
    def save(self, chapter: Chapter):
        pass

    @abstractmethod
    def find(self, chapter_id: ChapterId) -> Chapter:
        pass

    @abstractmethod
    def find_by_soundtrack(self, soundtrack_id: SoundtrackId) -> List[Chapter]:
        pass
    
    @abstractmethod
    def update(self, chapter_to_update: Chapter):
        pass

    @abstractmethod
    def delete(self, chapter_id: ChapterId):
        pass