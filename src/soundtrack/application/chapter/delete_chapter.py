from typing import List

from ...domain.chapter.chapter import Chapter
from ...domain.chapter.chapter_id import ChapterId
from ...domain.chapter.chapter_repository import ChapterRepository
from ...domain.chapter.exceptions.unexisting_chapter_error import UnexistingChapterError


class DeleteChapter():
    def __init__(self, chapter_repository: ChapterRepository):
        self.__chapter_repository = chapter_repository

    def run(self, chapter_id: ChapterId):

        chapter_to_be_deleted = self.__chapter_repository.find(chapter_id)
        if chapter_to_be_deleted == None:
            raise(UnexistingChapterError(chapter_id.value))

        self.__chapter_repository.delete(chapter_id)