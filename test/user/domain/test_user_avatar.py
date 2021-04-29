import pytest
from faker import Faker

from src.user.domain.user_avatar import UserAvatar

fake = Faker()


class TestUserAvatar():

    def test_from_url_constructor(self):
        user_avatar_url = "https://" + fake.pystr()
        user_avatar = UserAvatar.from_url(user_avatar_url)
        assert user_avatar.value == user_avatar_url

    def test_building_user_avatar_with_a_non_url_throws_an_error(self):
        user_avatar_url = fake.pystr()
        with pytest.raises(Exception):
            user_avatar == UserAvatar(user_avatar_url)
