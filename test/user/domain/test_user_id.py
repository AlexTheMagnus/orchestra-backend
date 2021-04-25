import pytest
from faker import Faker

fake = Faker()


class TestUserID():

    def test_from_string_constructor(self):
        str_user_id = faker.uuid4()
        user_id = UserId.fromString(str_user_id)
        self.assertEqual(user_id.value, str_user_id)
