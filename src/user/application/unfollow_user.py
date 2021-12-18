from ..domain.exceptions.unexisting_follow_error import UnexistingFollowError
from ..domain.user_id import UserId
from ..domain.user_repository import UserRepository

class UnfollowUser():
    def __init__(self, user_repository: UserRepository):
        self.__user_repository = user_repository

    def run(self, follower_id: UserId, user_to_unfollow_id: UserId):
        followed_users = self.__user_repository.get_followed_users(follower_id)

        if not any(user_to_unfollow_id.value == followed_user.user_id.value for followed_user in followed_users):
            raise(UnexistingFollowError(follower_id.value, user_to_unfollow_id.value))

        self.__user_repository.unfollow_user(follower_id, user_to_unfollow_id)
