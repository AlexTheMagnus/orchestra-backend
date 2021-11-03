import uuid
import pytest

from src.soundtrack.domain.exceptions.unexisting_soundtrack_error import UnexistingSoundtrackError
from src.soundtrack.domain.soundtrack import Soundtrack
from src.soundtrack.domain.soundtrack_id import SoundtrackId
from src.soundtrack.application.delete_soundtrack import DeleteSoundtrack
from ..builder.soundtrack_builder import SoundtrackBuilder
from ..builder.chapter_builder import ChapterBuilder
from ..infrastructure.soundtrack_in_memory_repository import SoundtrackInMemoryRepository
from ..infrastructure.chapter.chapter_in_memory_repository import ChapterInMemoryRepository

soundtrack_repository = SoundtrackInMemoryRepository()
chapter_repository = ChapterInMemoryRepository()
use_case: DeleteSoundtrack = DeleteSoundtrack(soundtrack_repository, chapter_repository)

class TestDeleteSoundtrackById():
    def test_soundtrack_is_deleted(self):
        soundtrack: Soundtrack = SoundtrackBuilder().build()
        soundtrack_repository.save(soundtrack)
        use_case.run(soundtrack.soundtrack_id)
        
        found_soundtrack: Soundtrack = soundtrack_repository.find(soundtrack.soundtrack_id)

        assert found_soundtrack == None

    def test_unexisting_soundtrack_id_raises_an_error(self):
        unregistered_soundtrack_id: SoundtrackId = SoundtrackId(str(uuid.uuid4()))

        with pytest.raises(UnexistingSoundtrackError):
            use_case.run(unregistered_soundtrack_id)

    def test_soundtrack_with_chapters_is_deleted(self):
            soundtrack: Soundtrack = SoundtrackBuilder().build()
            soundtrack_repository.save(soundtrack)
            chapter: Chapter = ChapterBuilder().with_soundtrack_id(soundtrack.soundtrack_id).build()
            chapter_repository.save(chapter)

            use_case.run(soundtrack.soundtrack_id)

            saved_chapter = chapter_repository.find(chapter.chapter_id)
            assert saved_chapter == None
            saved_soundtrack = soundtrack_repository.find(soundtrack.soundtrack_id)
            assert saved_soundtrack == None