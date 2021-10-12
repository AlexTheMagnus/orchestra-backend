from ...domain.chapter.chapter_repository import ChapterRepository
from ...domain.chapter.chapter import Chapter
from ...domain.chapter.exceptions.already_existing_chapter_error import AlreadyExistingChapterError

class AddChapter():
    def __init__(self, chapter_repository: ChapterRepository):
        self.__chapter_repository = chapter_repository

    def run(self, chapter: Chapter):

        if self.__chapter_repository.find(chapter.chapter_id):
            raise(AlreadyExistingChapterError(chapter.chapter_id.value))

        self.__chapter_repository.save(chapter)
