from .not_a_valid_url_error import NotAValidUrlError


class UserAvatar():

    def __init__(self, user_avatar: str):
        self.__validate_url_format(user_avatar)
        self.__value: str = user_avatar

    @staticmethod
    def from_url(avatar_url: str):
        return UserAvatar(avatar_url)

    @property
    def value(self):
        return self.__value

    def __validate_url_format(self, user_avatar: str):
        if not user_avatar.startswith('https://') and not user_avatar.startswith('http://'):
            raise NotAValidUrlError(user_avatar)
