from faker import Faker
from typing import List

from ..builder.user_builder import UserBuilder
from ..infrastructure.user_in_memory_repository import UserInMemoryRepository
from src.user.application.get_followed_users import GetFollowedUsers

fake = Faker()

user_repository = UserInMemoryRepository()
use_case = GetFollowedUsers(user_repository)

class TestGetFollowedUsers():

    def test_followed_users_are_getted(self):
        user = UserBuilder().build()
        user_repository.save(user)
        followed_user_list: List[User] = []

        for x in range(fake.random_number(1)):
            followed_user = UserBuilder().build()
            user_repository.save(followed_user)
            user_repository.save_follow(user.user_id, followed_user.user_id)
            followed_user_list.append(followed_user)

        found_followed_user_list: List[User] = use_case.run(user.user_id)

        assert len(found_followed_user_list) == len(followed_user_list)
        assert set(found_followed_user_list) == set(followed_user_list)


    def test_user_without_followed_users_returns_no_followed_users(self):
        user: User = UserBuilder().build()
        user_repository.save(user)

        found_followed_user_list: List[User] = use_case.run(user.user_id)
        assert len(found_followed_user_list) == 0


    def test_unexisting_user_returns_no_followed_users(self):
        user: User = UserBuilder().build()

        found_followed_user_list: List[User] = use_case.run(user.user_id)
        assert len(found_followed_user_list) == 0