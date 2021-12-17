from ..domain.user_id import UserId
from ..domain.user_repository import UserRepository
from ..domain.exceptions.unexisting_user_error import UnexistingUserError
from ..domain.exceptions.user_already_followed_error import UserAlreadyFollowedError

class FollowUser():
    def __init__(self, user_repository: UserRepository):
        self.__user_repository = user_repository

    def run(self, follower_id: UserId, followed_id: UserId):

        for user_id in [follower_id, followed_id]:
            if not self.__user_repository.find(user_id):
                raise(UnexistingUserError(user_id.value))

        for follower in self.__user_repository.get_followers(followed_id):
            if follower.user_id.value == follower_id.value:
                raise(UserAlreadyFollowedError(follower_id.value, followed_id.value))

        self.__user_repository.save_follow(follower_id, followed_id)