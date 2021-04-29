import pytest
from faker import Faker

from src.user.domain.user_id import UserId

fake = Faker()


class TestUserID():

    def test_from_string_constructor(self):
        str_user_id = fake.pystr()
        user_id = UserId.from_string(str_user_id)
        assert user_id.value == str_user_id
