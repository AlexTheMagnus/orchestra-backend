import pytest
import uuid

from ...builder.chapter_builder import ChapterBuilder
from ...builder.soundtrack_builder import SoundtrackBuilder
from ...infrastructure.chapter.chapter_in_memory_repository import ChapterInMemoryRepository
from ...infrastructure.soundtrack_in_memory_repository import SoundtrackInMemoryRepository
from src.soundtrack.application.chapter.delete_chapter import DeleteChapter
from src.soundtrack.domain.chapter.chapter_id import ChapterId
from src.soundtrack.domain.chapter.exceptions.unexisting_chapter_error import UnexistingChapterError

soundtrack_repository = SoundtrackInMemoryRepository()
chapter_repository = ChapterInMemoryRepository()
use_case = DeleteChapter(chapter_repository)

class TestDeleteChapterById():
    def test_chapter_is_deleted(self):
        soundtrack = SoundtrackBuilder().build()
        soundtrack_repository.save(soundtrack)
        chapter = ChapterBuilder().build()
        chapter_repository.save(chapter)

        use_case.run(chapter.chapter_id)
        
        found_chapter = chapter_repository.find(chapter.chapter_id)

        assert found_chapter == None

    def test_unexisting_chapter_id_raises_an_error(self):
        unregistered_chapter_id = ChapterId.from_string((str(uuid.uuid4())))

        with pytest.raises(UnexistingChapterError):
            use_case.run(unregistered_chapter_id)