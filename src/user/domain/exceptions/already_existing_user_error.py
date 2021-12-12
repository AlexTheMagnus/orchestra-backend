from ..user_id import UserId

class AlreadyExistingUserError(Exception):
    def __init__(self, user_id: UserId):
        self.message = 'Register user: user with id {0} already exists'.format(
            user_id.value)

    def __str__(self):
        return self.message
