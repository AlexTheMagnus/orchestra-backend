import pytest
import uuid

from src.soundtrack.domain.soundtrack_id import SoundtrackId
from src.soundtrack.domain.not_a_valid_soundtrack_id_error import NotAValidSoundtrackIdError


class TestSoundtrackId():

    def test_from_string_constructor(self):
        str_soundtrack_id = str(uuid.uuid4())
        soundtrack_id = SoundtrackId.from_string(str_soundtrack_id)
        assert soundtrack_id.value == str_soundtrack_id

    def test_building_soundtrack_id_with_a_non_uuid4_throws_an_error(self):
        str_soundtrack_id = str(uuid.uuid1())
        with pytest.raises(NotAValidSoundtrackIdError):
            soundtrack_id = SoundtrackId.from_string(str_soundtrack_id)
