import uuid
from faker import Faker

from src.soundtrack.infrastructure.validators.soundtracks_user_get_validator import SoundtracksUserGetValidator

fake = Faker()


class TestSoundtracksUserGetValidator():
    def test_correct_case_all_attributes(self):
        author_to_get_soundtracks = {
            "author": str(uuid.uuid4()),
        }

        assert SoundtracksUserGetValidator().validate(author_to_get_soundtracks) == True

    def test_wrong_case_not_correct_types(self):
        author_to_get_soundtracks = {
            "author": 125,
        }

        assert SoundtracksUserGetValidator().validate(author_to_get_soundtracks) == False
