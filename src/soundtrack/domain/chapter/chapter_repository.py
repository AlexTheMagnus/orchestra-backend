from abc import ABC, abstractmethod
from typing import List

from .chapter import Chapter
from .chapter_id import ChapterId
from ..soundtrack_id import SoundtrackId


class ChapterRepository(ABC):
    @abstractmethod
    def save(self, chapter: Chapter):
        pass

    def find(self, chapter_id: ChapterId) -> Chapter:
        pass

    def find_by_soundtrack(self, soundtrack_id: SoundtrackId) -> List[Chapter]:
        pass
    
    def delete(self, chapter_id: ChapterId):
        pass