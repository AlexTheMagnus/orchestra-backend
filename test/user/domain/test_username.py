import pytest
from faker import Faker

from src.user.domain.username import Username

fake = Faker()


class TestUsername():

    def test_from_string_constructor(self):
        str_username = fake.name()
        username = Username.from_string(str_username)
        assert username.value == str_username
