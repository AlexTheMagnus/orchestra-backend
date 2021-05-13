import pytest
from faker import Faker

from src.user.domain.user import User
from src.user.domain.user_id import UserId
from src.user.domain.soundtrack_id import SoundtrackId

fake = Faker()


class TestUser():

    def test_user_constructor(self):
        user_id = UserId.from_string(fake.pystr())
        favorites = []
        likes = []

        user = User(user_id, favorites, likes)

        assert user.user_id == user_id
        assert user.favorites == favorites
        assert user.likes == likes

    def test_get_id(self):
        user_id = UserId.from_string(fake.pystr())
        favorites = []
        likes = []

        user = User(user_id, favorites, likes)

        assert user.get_id() == user_id
