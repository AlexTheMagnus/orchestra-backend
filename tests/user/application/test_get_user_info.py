import pytest
import uuid
from faker import Faker
from typing import List

from ..infrastructure.user_in_memory_repository import UserInMemoryRepository
from src.user.domain.user_id import UserId
from src.user.domain.user import User
from ..builder.user_builder import UserBuilder
from src.user.application.get_user_info import GetUserInfo

fake = Faker()

user_repository = UserInMemoryRepository()
use_case: GetUserInfo = GetUserInfo(user_repository)


class TestGetUserInfo():
    def test_user_info_is_getted(self):
        user: User = UserBuilder().build()
        user_repository.save(user)

        found_user: User = use_case.run(user.user_id)
        assert found_user.user_id.value == user.user_id.value
        assert found_user.username.value == user.username.value
        assert found_user.user_avatar.value == user.user_avatar.value

    def test_non_registered_user_info_is_asked(self):
        non_registered_user: User = UserBuilder().build()

        found_user: User = use_case.run(non_registered_user.user_id)
        assert found_user == None