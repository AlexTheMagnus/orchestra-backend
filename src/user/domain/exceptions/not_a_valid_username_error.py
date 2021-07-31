class NotAValidUsernameError(Exception):
    def __init__(self, username: str):
        self.message = '{0} is not a valid username.'.format(
            username)

    def __str__(self):
        return self.message
