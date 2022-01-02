from .exceptions.not_a_valid_url_error import NotAValidUrlError


class UserAvatar():

    def __init__(self, user_avatar: str):
        self.__validate_url_format(user_avatar)
        self.__value: str = user_avatar

    @staticmethod
    def from_url(user_avatar_url: str):
        return UserAvatar(user_avatar_url)

    @property
    def value(self):
        return self.__value

    def __validate_url_format(self, user_avatar_url: str):
        if not user_avatar_url.startswith("https://") and \
            not user_avatar_url.startswith("http://") and \
            not user_avatar_url == "":
                raise(NotAValidUrlError(user_avatar_url))
