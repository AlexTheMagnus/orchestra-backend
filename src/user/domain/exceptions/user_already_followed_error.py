from ..user_id import UserId

class UserAlreadyFollowedError(Exception):
    def __init__(self, follower_id: str, followed_id: str):
        self.message = 'The user {0} is already been followed by the user {1}'.format(
            followed_id, follower_id)

    def __str__(self):
        return self.message
