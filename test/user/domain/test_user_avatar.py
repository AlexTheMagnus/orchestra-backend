import pytest
from faker import Faker

fake = Faker()


class TestUserAvatar():

    def test_from_url_constructor(self):
        user_avatar_url = fake.image_url()
        user_avatar = UserAvatar.fromURL(user_avatar_url)
        self.assertEqual(user_avatar.value, user_avatar_url)

    def test_building_user_avatar_with_a_non_uuid4_throws_an_error(self):
        str_user_id = str(uuid.uuid1())
        with self.assertRaises(TypeError):
            user_id = UserId(str_user_id)
