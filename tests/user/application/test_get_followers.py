from faker import Faker
from typing import List

from ..builder.user_builder import UserBuilder
from ..infrastructure.user_in_memory_repository import UserInMemoryRepository
from src.user.application.get_followers import GetFollowers

fake = Faker()

user_repository = UserInMemoryRepository()
use_case = GetFollowers(user_repository)

class TestGetFollowers():

    def test_followers_are_getted(self):
        user = UserBuilder().build()
        user_repository.save(user)
        follower_list: List[User] = []

        for x in range(fake.random_number(1)):
            follower: User = UserBuilder().build()
            user_repository.save(follower)
            user_repository.save_follow(follower.user_id, user.user_id)
            follower_list.append(follower)

        found_follower_list: List[User] = use_case.run(user.user_id)

        assert len(found_follower_list) == len(follower_list)
        assert set(found_follower_list) == set(follower_list)


    def test_user_without_followers_returns_no_followers(self):
        user: User = UserBuilder().build()
        user_repository.save(user)

        found_follower_list: List[User] = use_case.run(user.user_id)
        assert len(found_follower_list) == 0


    def test_unexisting_user_returns_no_followers(self):
        user: User = UserBuilder().build()

        found_follower_list: List[User] = use_case.run(user.user_id)
        assert len(found_follower_list) == 0