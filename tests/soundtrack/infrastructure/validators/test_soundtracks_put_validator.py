import uuid
from faker import Faker

from src.soundtrack.infrastructure.validators.soundtracks_put_validator import SoundtracksPutValidator

fake = Faker()


class TestSoundtracksPutValidator():
    def test_correct_case_all_attributes(self):
        soundtrack_to_update = {
            "book": "978-2-1550-9533-9",
            "soundtrack_title": fake.pystr()
        }

        assert SoundtracksPutValidator().validate(soundtrack_to_update) == True

    def test_correct_case_not_all_attributes(self):
        soundtrack_to_update = {
            "soundtrack_title": fake.pystr()
        }

        assert SoundtracksPutValidator().validate(soundtrack_to_update) == True

    def test_wrong_case_not_correct_types(self):
        soundtrack_to_update = {
            "book": fake.random_number(2),
            "soundtrack_title": fake.random_number(2)
        }

        assert SoundtracksPutValidator().validate(soundtrack_to_update) == False
