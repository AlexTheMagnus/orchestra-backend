import pytest
from faker import Faker

from src.user.domain.user import User
from src.user.domain.user_id import UserId
from src.user.domain.email import Email
from src.user.domain.username import Username
from src.user.domain.avatar import Avatar


fake = Faker()


class TestUserID():

    def test_user_constructor(self):
        user_id = UserId.from_string(fake.pystr())
        email = Email.from_string(fake.email())
        username = Username.from_string(fake.name())
        avatar = Avatar.from_url("http://" + fake.pystr())

        user = User(user_id, email, username, avatar)

        assert user.user_id == user_id
        assert user.email == email
        assert user.username == username
        assert user.avatar == avatar

    def test_get_id(self):
        user_id = UserId.from_string(fake.pystr())
        email = Email.from_string(fake.email())
        username = Username.from_string(fake.name())
        avatar = Avatar.from_url("http://" + fake.pystr())

        user = User(user_id, email, username, avatar)

        assert user.get_id() == user_id
