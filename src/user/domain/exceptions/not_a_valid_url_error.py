class NotAValidUrlError(Exception):
    def __init__(self, url: str):
        self.message = '{0} is not a valid url.'.format(url)

    def __str__(self):
        return self.message
