import pytest
from faker import Faker

from src.user.domain.email import Email
from src.user.domain.not_a_valid_email_error import NotAValidEmailError

fake = Faker()


class TestEmail():

    def test_from_string_constructor(self):
        str_email = fake.email()
        email = Email.from_string(str_email)
        assert email.value == str_email

    def test_building_email_with_a_non_valid_email_raise_an_error(self):
        str_email = fake.pystr()

        with pytest.raises(NotAValidEmailError):
            Email.from_string(str_email)
