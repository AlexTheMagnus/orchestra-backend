import uuid
import pytest

from src.soundtrack.application.get_soundtrack_by_id import GetSoundtrackById
from src.soundtrack.domain.exceptions.unexisting_soundtrack_error import UnexistingSoundtrackError
from src.soundtrack.domain.soundtrack import Soundtrack
from src.soundtrack.domain.soundtrack_id import SoundtrackId
from ..builder.soundtrack_builder import SoundtrackBuilder
from ..infrastructure.soundtrack_in_memory_repository import SoundtrackInMemoryRepository

soundtrack_repository = SoundtrackInMemoryRepository()
use_case: GetSoundtrackById = GetSoundtrackById(soundtrack_repository)
soundtrack_id: SoundtrackId = SoundtrackId(str(uuid.uuid4()))
soundtrack: Soundtrack = SoundtrackBuilder().with_soundtrack_id(soundtrack_id).build()
soundtrack_repository.save(soundtrack)

class TestGetSoundtrackById():
    def test_soundtrack_is_getted(self):
        found_soundtrack: Soundtrack = use_case.run(soundtrack_id)
        
        assert found_soundtrack != None
        assert found_soundtrack.soundtrack_id == soundtrack.soundtrack_id
        assert found_soundtrack.book == soundtrack.book
        assert found_soundtrack.soundtrack_title == soundtrack.soundtrack_title
        assert found_soundtrack.author == soundtrack.author

    def test_unexisting_soundtrack_id_returns_no_soundtrack(self):
        unregistered_soundtrack_id: SoundtrackId = SoundtrackId(str(uuid.uuid4()))

        with pytest.raises(UnexistingSoundtrackError):
            use_case.run(unregistered_soundtrack_id)