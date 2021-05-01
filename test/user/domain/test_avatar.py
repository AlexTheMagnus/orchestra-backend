import pytest
from faker import Faker

from src.user.domain.avatar import Avatar
from src.user.domain.not_a_valid_url_error import NotAValidUrlError

fake = Faker()


class TestAvatar():

    def test_from_url_constructor(self):
        avatar_url = "https://" + fake.pystr()
        avatar = Avatar.from_url(avatar_url)
        assert avatar.value == avatar_url

    def test_building_avatar_with_a_non_valid_url_throws_an_error(self):
        avatar_url = fake.pystr()

        with pytest.raises(NotAValidUrlError):
            Avatar.from_url(avatar_url)
