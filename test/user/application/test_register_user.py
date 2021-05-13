import pytest
from faker import Faker

from test.user.infrastructure.user_in_memory_repository import UserInMemoryRepository
from test.user.builder.user_builder import UserBuilder
from src.user.application.register_user import RegisterUser
from src.user.domain.user_id import UserId
from src.user.domain.user import User
from src.user.domain.already_existing_user_error import AlreadyExistingUserError

fake = Faker()


user_repository = UserInMemoryRepository()
use_case: RegisterUser = RegisterUser(user_repository)

user_id: UserId = UserId.from_string(fake.pystr())


class TestRegisterUser():

    def test_new_user_is_registered(self):
        user: User = UserBuilder().with_user_id(
            user_id).with_favorites([]).with_likes([]).build()

        use_case.run(user)

        found_user = user_repository.find(user_id)
        assert found_user.user_id.value == user_id.value
        assert found_user.favorites == favorites.value
        assert found_user.likes == likes.value

    def test_already_existing_user_throws_an_error(self):
        user: User = UserBuilder().with_user_id(
            user_id).with_favorites([]).with_likes([])

        with pytest.raises(AlreadyExistingUserError):
            use_case.run(user)
