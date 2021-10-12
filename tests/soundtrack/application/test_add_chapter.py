import pytest
from faker import Faker

from ..infrastructure.chapter.chapter_in_memory_repository import ChapterInMemoryRepository
from ..infrastructure.soundtrack_in_memory_repository import SoundtrackInMemoryRepository
from src.soundtrack.application.chapter.add_chapter import AddChapter
from src.soundtrack.domain.soundtrack import Soundtrack
from ..builder.soundtrack_builder import SoundtrackBuilder
from ..builder.chapter_builder import ChapterBuilder
from src.soundtrack.domain.chapter.chapter import Chapter
from src.soundtrack.domain.chapter.exceptions.already_existing_chapter_error import AlreadyExistingChapterError
from src.soundtrack.domain.exceptions.unexisting_soundtrack_error import UnexistingSoundtrackError

chapter_repository = ChapterInMemoryRepository()
soundtrack_repository = SoundtrackInMemoryRepository()
soundtrack: Soundtrack = SoundtrackBuilder().build()
soundtrack_repository.save(soundtrack)
use_case: AddChapter = AddChapter(chapter_repository, soundtrack_repository)
chapter: Chapter = ChapterBuilder().with_soundtrack_id(soundtrack.soundtrack_id).build()

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

    def test_non_existing_soundtrack_throws_an_error(self):
      new_chapter: Chapter = ChapterBuilder().build()

      with pytest.raises(UnexistingSoundtrackError):
          use_case.run(new_chapter)
