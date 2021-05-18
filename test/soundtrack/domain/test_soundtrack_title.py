import pytest
from faker import Faker

from src.soundtrack.domain.soundtrack_title import SoundtrackTitle
from src.soundtrack.domain.not_a_valid_soundtrack_title_error import NotAValidSoundtrackTitleError

fake = Faker()


class SountrackTitle():

    def test_from_string_constructor(self):
        str_soundtrack_title = fake.pystr()
        soundtrack_title = SoundtrackTitle.from_string(str_soundtrack_title)
        assert soundtrack_title.value == str_soundtrack_title

    def test_building_soundtrack_title_with_an_extra_spaced_string(self):
        str_soundtrack_title = SoundtrackTitle.from_string(
            "  extraSpacedSountrackTitle   ")
        soundtrack_title = SoundtrackTitle.from_string(str_soundtrack_title)
        assert soundtrack_title.value == "extraSpacedSountrackTitle"

    def test_building_soundtrack_title_with_an_empty_string_throws_an_error(self):
        with pytest.raises(NotAValidSoundtrackTitleError):
            soundtrack_title = SoundtrackTitle.from_string("")

    def test_building_soundtrack_title_with_string_filled_with_spaces_throws_an_error(self):
        with pytest.raises(NotAValidSoundtrackTitleError):
            soundtrack_title = SoundtrackTitle.from_string("   ")
