class NotAValidUrlError(Exception):
    def __init__(self, avatar_url: str):
        self.message = 'Avatar: {0} is not a valid url.'.format(
            avatar_url)

    def __str__(self):
        return self.message
