from uuid import UUID
from ....src.soundtrack.domain.soundtrack_id import SoundtrackId


class TestSoundtrackId(unittest.TestCase):

    def test_from_string_constructor(self):
        str_soundtrack_id = str(uuid.uuid4())
        soundtrack_id = SoundtrackId.from_string(str_soundtrack_id)
        assert soundtrack_id.value == str_soundtrack_id

    def test_building_soundtrack_id_with_a_non_uuid4_throws_an_error(self):
        str_soundtrack_id = str(uuid.uuid1())
        with pytest.raises(NotAValidSountrackIdError):
            soundtrack_id = SoundtrackId(str_soundtrack_id)
