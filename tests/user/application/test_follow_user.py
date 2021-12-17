import pytest

from ..builder.user_builder import UserBuilder
from ..infrastructure.user_in_memory_repository import UserInMemoryRepository
from src.user.application.follow_user import FollowUser
from src.user.domain.exceptions.unexisting_user_error import UnexistingUserError
from src.user.domain.exceptions.user_already_followed_error import UserAlreadyFollowedError
from src.user.domain.user import User

user_repository = UserInMemoryRepository()
use_case = FollowUser(user_repository)

class TestFollowUser():

    def test_user_is_followed(self):
        follower_user = UserBuilder().build()
        user_repository.save(follower_user)
        followed_user = UserBuilder().build()
        user_repository.save(followed_user)

        use_case.run(follower_user.user_id, followed_user.user_id)

        found_followers: List[User] = user_repository.get_followers(followed_user.user_id)
        assert len(found_followers) == 1
        assert found_followers == [follower_user]


    def test_user_follows_unexisting_user(self):
        follower_user = UserBuilder().build()
        user_repository.save(follower_user)
        followed_user = UserBuilder().build()

        with pytest.raises(UnexistingUserError):
            use_case.run(follower_user.user_id, followed_user.user_id)


    def test_unexisting_user_follows_user(self):
        follower_user = UserBuilder().build()
        followed_user = UserBuilder().build()
        user_repository.save(followed_user)

        with pytest.raises(UnexistingUserError):
            use_case.run(follower_user.user_id, followed_user.user_id)


    def test_follow_same_user_twice_throws_an_error(self):
        follower_user = UserBuilder().build()
        user_repository.save(follower_user)
        followed_user = UserBuilder().build()
        user_repository.save(followed_user)

        user_repository.save_follow(follower_user.user_id, followed_user.user_id)

        with pytest.raises(UserAlreadyFollowedError):
            use_case.run(follower_user.user_id, followed_user.user_id)