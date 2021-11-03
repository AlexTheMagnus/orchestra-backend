from typing import List

from ..domain.soundtrack_repository import SoundtrackRepository
from ..domain.chapter.chapter_repository import ChapterRepository
from ..domain.soundtrack_id import SoundtrackId
from ..domain.exceptions.unexisting_soundtrack_error import UnexistingSoundtrackError
from ..domain.chapter.chapter import Chapter

class DeleteSoundtrack():
    def __init__(self, soundtrack_repository: SoundtrackRepository, chapter_repository: ChapterRepository):
        self.__soundtrack_repository = soundtrack_repository
        self.__chapter_repository = chapter_repository

    def run(self, soundtrack_id: SoundtrackId):
        soundtrack_chapters: List[Chapter] = self.__chapter_repository.find_by_soundtrack(soundtrack_id)
        for chapter in soundtrack_chapters:
            self.__chapter_repository.delete(chapter.chapter_id)

        soundtrack_to_be_deleted = self.__soundtrack_repository.find(soundtrack_id)
        if soundtrack_to_be_deleted == None:
            raise(UnexistingSoundtrackError(soundtrack_id.value))

        self.__soundtrack_repository.delete(soundtrack_id)
