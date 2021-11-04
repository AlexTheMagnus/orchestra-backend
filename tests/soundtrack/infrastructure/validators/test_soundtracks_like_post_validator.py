import uuid
from faker import Faker

from src.soundtrack.infrastructure.validators.soundtracks_like_post_validator import SoundtracksLikePostValidator

fake = Faker()


class TestLikePostValidator():
    def test_correct_case_all_attributes(self):
        soundtrack_to_like = {
            "user_id": str(uuid.uuid4()),
            "soundtrack_id": str(uuid.uuid4())
        }

        assert SoundtracksLikePostValidator().validate(soundtrack_to_like) == True

    def test_wrong_case_not_all_attributes(self):
        soundtrack_to_like = {
            "user_id": str(uuid.uuid4())
        }

        assert SoundtracksLikePostValidator().validate(soundtrack_to_like) == False

    def test_wrong_case_not_correct_types(self):
        soundtrack_to_like = {
            "user_id": str(uuid.uuid4()),
            "soundtrack_id": fake.random_number(2)
        }

        assert SoundtracksLikePostValidator().validate(soundtrack_to_like) == False
