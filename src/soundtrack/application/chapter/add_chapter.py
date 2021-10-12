from ...domain.chapter.chapter_repository import ChapterRepository
from ...domain.soundtrack_repository import SoundtrackRepository
from ...domain.chapter.chapter import Chapter
from ...domain.chapter.exceptions.already_existing_chapter_error import AlreadyExistingChapterError
from ...domain.exceptions.unexisting_soundtrack_error import UnexistingSoundtrackError

class AddChapter():
    def __init__(self, chapter_repository: ChapterRepository, soundtrack_repository: SoundtrackRepository):
        self.__chapter_repository = chapter_repository
        self.__soundtrack_repository = soundtrack_repository

    def run(self, chapter: Chapter):

        if self.__chapter_repository.find(chapter.chapter_id):
            raise(AlreadyExistingChapterError(chapter.chapter_id.value))
        
        if not self.__soundtrack_repository.find(chapter.soundtrack_id):
            raise(UnexistingSoundtrackError(chapter.soundtrack_id.value))

        self.__chapter_repository.save(chapter)
