import pytest
from faker import Faker

from src.user.domain.user import User
from src.user.domain.user_id import UserId
from src.user.domain.username import Username
from src.user.domain.user_avatar import UserAvatar

fake = Faker()


class TestUser():

    def test_user_constructor(self):
        user_id = UserId.from_string(fake.pystr())
        username = Username.from_string(fake.name())
        user_avatar = UserAvatar.from_url("https://" + fake.pystr())

        user = User(user_id, username, user_avatar)

        assert user.user_id == user_id
        assert user.username == username
        assert user.user_avatar == user_avatar