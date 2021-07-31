import pytest
from faker import Faker

from src.user.domain.username import Username
from src.user.domain.exceptions.not_a_valid_username_error import NotAValidUsernameError

fake = Faker()


class TestUsername():

    def test_from_string_constructor(self):
        str_username = fake.pystr()
        username = Username.from_string(str_username)
        assert username.value == str_username

    def test_building_username_with_an_extra_spaced_string(self):
        str_username = "  extraSpacedUsername   "
        username = Username.from_string(str_username)
        assert username.value == "extraSpacedUsername"

    def test_building_username_with_an_empty_string_throws_an_error(self):
        with pytest.raises(NotAValidUsernameError):
            username = Username.from_string("")

    def test_building_username_with_string_filled_with_spaces_throws_an_error(self):
        with pytest.raises(NotAValidUsernameError):
            username = Username.from_string("   ")
