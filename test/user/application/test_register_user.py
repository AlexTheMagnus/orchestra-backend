import pytest
from faker import Faker

from test.user.infrastructure.user_in_memory_repository import UserInMemoryRepository
from src.user.application.register_user import RegisterUser
from src.user.domain.user_id import UserId
from src.user.domain.email import Email
from src.user.domain.username import Username
from src.user.domain.avatar import Avatar
from src.user.domain.user import User
from test.user.builder.user_builder import UserBuilder
from src.user.domain.already_existing_user_error import AlreadyExistingUserError

fake = Faker()


user_repository = UserInMemoryRepository()
use_case: RegisterUser = RegisterUser(user_repository)

user_id: UserId = UserId.from_string(fake.pystr())
email = Email.from_string(fake.email())
username = Username.from_string(fake.name())
avatar = Avatar.from_url("https://" + fake.pystr())


class TestRegisterUser():

    def test_new_user_is_registered(self):
        user: User = UserBuilder().with_user_id(user_id).with_email(
            email).with_username(username).with_avatar(avatar)

        use_case.run(user)

        found_user = user_repository.find(user_id)
        assert found_user.user_id.value == user_id.value
        assert found_user.email.value == email.value
        assert found_user.username.value == username.value
        assert found_user.avatar.value == avatar.value

    def test_already_existing_user_throws_an_error(self):
        user: User = UserBuilder().with_user_id(user_id).with_email(
            email).with_username(username).with_avatar(avatar)

        with pytest.raises(AlreadyExistingUserError):
            use_case.run(user)
