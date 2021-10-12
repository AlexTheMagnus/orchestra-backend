import pytest
from faker import Faker

from ..builder.chapter_builder import ChapterBuilder
from ..infrastructure.chapter.chapter_in_memory_repository import ChapterInMemoryRepository
from src.soundtrack.domain.chapter.chapter import Chapter
from src.soundtrack.application.chapter.add_chapter import AddChapter
from src.soundtrack.domain.chapter.exceptions.already_existing_chapter_error import AlreadyExistingChapterError

chapter_repository = ChapterInMemoryRepository()
use_case: AddChapter = AddChapter(chapter_repository)
chapter: Chapter = ChapterBuilder().build()

class TestAddChapter():

    def test_new_chapter_is_added(self): 
        use_case.run(chapter)

        found_chapter: Chapter = chapter_repository.find(
            chapter.chapter_id)
        assert found_chapter != None
        assert found_chapter.chapter_id.value == chapter.chapter_id.value
        assert found_chapter.soundtrack_id.value == chapter.soundtrack_id.value
        assert found_chapter.chapter_number.value == chapter.chapter_number.value
        assert found_chapter.theme.value == chapter.theme.value
        assert found_chapter.chapter_title.value == chapter.chapter_title.value

    def test_already_existing_chapter_throws_an_error(self):
        with pytest.raises(AlreadyExistingChapterError):
            use_case.run(chapter)
