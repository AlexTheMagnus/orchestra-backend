class AlreadyExistingUserError(Exception):
    def __init__(self, email: str):
        self.message = 'Register user: user with email {0} already exists'.format(
            email)

    def __str__(self):
        return self.message
