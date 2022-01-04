from typing import List, Optional

from src.soundtrack.domain.chapter.chapter_repository import ChapterRepository
from src.soundtrack.domain.chapter.chapter import Chapter
from src.soundtrack.domain.chapter.chapter_id import ChapterId
from src.soundtrack.domain.soundtrack_id import SoundtrackId

class ChapterInMemoryRepository(ChapterRepository):
    def __init__(self):
        self.__chapters: List[Chapter] = []

    def save(self, chapter: Chapter):
        self.__chapters.append(chapter)

    def find(self, chapter_id: ChapterId) -> Optional[Chapter]:
        for chapter in self.__chapters:
            if chapter.chapter_id.value == chapter_id.value:
                return chapter

        return None

    def find_by_soundtrack(self, soundtrack_id: SoundtrackId):
        found_chapters: List[Chapter] = []

        for chapter in self.__chapters:
            if chapter.soundtrack_id.value == soundtrack_id.value:
                found_chapters.append(chapter)
                
        return found_chapters

    def update(self, chapter_to_update: Chapter):
        for chapter in self.__chapters:
            if chapter.chapter_id.value == chapter_to_update.chapter_id.value:
                self.__chapters.remove(chapter)
        self.__chapters.append(chapter_to_update)

    def delete(self, chapter_id: ChapterId):
        self.__chapters = [chapter for chapter in self.__chapters if chapter.chapter_id != chapter_id]
