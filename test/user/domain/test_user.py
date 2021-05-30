import pytest
from faker import Faker

from src.user.domain.user import User
from src.user.domain.user_id import UserId

fake = Faker()


class TestUser():

    def test_user_constructor(self):
        user_id = UserId.from_string(fake.pystr())
        favorites = []
        likes = []
        soundtracks = []
        following = []
        followers = []

        user = User(user_id, favorites, likes,
                    soundtracks, following, followers)

        assert user.user_id == user_id
        assert user.favorites == favorites
        assert user.likes == likes
        assert user.soundtracks == soundtracks
        assert user.followers == followers
        assert user.following == following

    def test_get_id(self):
        user_id = UserId.from_string(fake.pystr())
        favorites = []
        likes = []
        soundtracks = []
        following = []
        followers = []

        user = User(user_id, favorites, likes,
                    soundtracks, following, followers)

        assert user.get_id() == user_id
