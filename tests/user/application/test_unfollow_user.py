from typing import List
import pytest
import uuid

from ..builder.user_builder import UserBuilder
from ..infrastructure.user_in_memory_repository import UserInMemoryRepository
from src.user.application.unfollow_user import UnfollowUser
from src.user.domain.exceptions.unexisting_follow_error import UnexistingFollowError
from src.user.domain.user import User
from src.user.domain.user_id import UserId

user_repository = UserInMemoryRepository()
use_case = UnfollowUser(user_repository)


class TestUnfollowUser():

    def test_user_is_unfollowed(self):
        follower = UserBuilder().build()
        user_repository.save(follower)
        user_to_unfollow = UserBuilder().build()
        user_repository.save(user_to_unfollow)
        user_repository.save_follow(follower.user_id, user_to_unfollow.user_id)
        user_keep_following = UserBuilder().build()
        user_repository.save(user_keep_following)
        user_repository.save_follow(follower.user_id, user_keep_following.user_id)

        use_case.run(follower.user_id, user_to_unfollow.user_id)

        found_followers: List[User] = user_repository.get_followed_users(follower.user_id)
        assert len(found_followers) == 1
        assert found_followers[0].user_id.value == user_keep_following.user_id.value
        assert found_followers[0].username.value == user_keep_following.username.value
        assert found_followers[0].user_avatar.value == user_keep_following.user_avatar.value


    def test_unfollowing_a_non_followed_user_raises_an_error(self):
        follower_id = UserId.from_string(str(uuid.uuid4()))
        user_to_unfollow_id = UserId.from_string(str(uuid.uuid4()))

        with pytest.raises(UnexistingFollowError):
            use_case.run(follower_id, user_to_unfollow_id)