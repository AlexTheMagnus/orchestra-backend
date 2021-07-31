import uuid
from faker import Faker

from src.soundtrack.infrastructure.validators.soundtrack_post_validator import SoundtracksPostValidator

fake = Faker()


class TestSoundtracksPostValidator():
    def test_correct_case_all_attributes(self):
        soundtrack_to_save = {
            "soundtrack_id": str(uuid.uuid4()),
            "book": "978-2-1550-9533-9",
            "soundtrack_title": fake.pystr(),
            "author": str(uuid.uuid4()),
        }

        assert SoundtracksPostValidator().validate(soundtrack_to_save) == True

    def test_wrong_case_not_all_attributes(self):
        soundtrack_to_save = {
            "soundtrack_id": str(uuid.uuid4()),
            "book": "978-2-1550-9533-9",
        }

        assert SoundtracksPostValidator().validate(soundtrack_to_save) == False

    def test_wrong_case_not_correct_types(self):
        soundtrack_to_save = {
            "soundtrack_id": fake.pystr(),
            "book": str(uuid.uuid4()),
            "soundtrack_title": 25,
            "author": 123,
        }

        assert SoundtracksPostValidator().validate(soundtrack_to_save) == False
