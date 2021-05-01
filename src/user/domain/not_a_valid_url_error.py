class NotAValidUrlError(Exception):
    def __init__(self, user_avatar_url: str):
        self.message = 'User avatar: {0} is not a valid url.'.format(
            user_avatar_url)

    def __str__(self):
        return self.message
