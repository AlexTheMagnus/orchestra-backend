import uuid
import pytest

from src.soundtrack.domain.exceptions.unexisting_soundtrack_error import UnexistingSoundtrackError
from src.soundtrack.domain.soundtrack import Soundtrack
from src.soundtrack.domain.soundtrack_id import SoundtrackId
from src.soundtrack.application.delete_soundtrack import DeleteSoundtrack
from ..builder.soundtrack_builder import SoundtrackBuilder
from ..infrastructure.soundtrack_in_memory_repository import SoundtrackInMemoryRepository

soundtrack_repository = SoundtrackInMemoryRepository()
use_case: DeleteSoundtrack = DeleteSoundtrack(soundtrack_repository)
soundtrack: Soundtrack = SoundtrackBuilder().build()
soundtrack_repository.save(soundtrack)

class TestDeleteSoundtrackById():
    def test_soundtrack_is_deleted(self):
        use_case.run(soundtrack.soundtrack_id)
        
        found_soundtrack: Soundtrack = soundtrack_repository.find(soundtrack.soundtrack_id)

        assert found_soundtrack == None


    def test_unexisting_soundtrack_id_raises_an_error(self):
        unregistered_soundtrack_id: SoundtrackId = SoundtrackId(str(uuid.uuid4()))

        with pytest.raises(UnexistingSoundtrackError):
            use_case.run(unregistered_soundtrack_id)