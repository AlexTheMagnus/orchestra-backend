from .not_a_valid_url_error import NotAValidUrlError


class Avatar():

    def __init__(self, avatar_url: str):
        self.__validate_url_format(avatar_url)
        self.__value: str = avatar_url

    @staticmethod
    def from_url(avatar_url: str):
        return Avatar(avatar_url)

    @property
    def value(self):
        return self.__value

    def __validate_url_format(self, avatar_url: str):
        if not avatar_url.startswith('https://') and not avatar_url.startswith('http://'):
            raise NotAValidUrlError(avatar_url)
