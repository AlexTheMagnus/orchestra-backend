from typing import TypedDict, Union

from ...domain.chapter.chapter_repository import ChapterRepository
from ...domain.chapter.chapter import Chapter
from ...domain.chapter.chapter_id import ChapterId
from ...domain.chapter.exceptions.unexisting_chapter_error import UnexistingChapterError

class NewChapterData(TypedDict):
    chapter_number: Union[int, None]
    theme: Union[str, None]
    chapter_title: Union[str, None]

class UpdateChapter():
    def __init__(self, chapter_repository: ChapterRepository):
        self.__chapter_repository = chapter_repository

    def run(self, chapter_id: ChapterId, new_data: NewChapterData):
        found_chapter = self.__chapter_repository.find(chapter_id)
        if not found_chapter:
            raise(UnexistingChapterError(chapter_id.value))

        chapter_number = new_data['chapter_number'] if new_data['chapter_number'] else found_chapter.chapter_number
        theme = new_data['theme'] if new_data['theme'] else found_chapter.theme
        chapter_title = new_data['chapter_title'] if new_data['chapter_title'] else found_chapter.chapter_title

        updated_chapter: Chapter = Chapter(
            found_chapter.chapter_id, found_chapter.soundtrack_id, chapter_number, theme, chapter_title
        )

        self.__chapter_repository.update(updated_chapter)