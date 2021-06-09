from .exceptions.not_a_valid_theme_url_error import NotAValidThemeUrlError


class Theme():

    def __init__(self, theme: str):
        self.__validate_theme_url_format(theme)
        self.__value: str = theme

    @staticmethod
    def from_url(theme_url: str):
        return Theme(theme_url)

    @property
    def value(self):
        return self.__value

    def __validate_theme_url_format(self, theme_url: str):
        if not theme_url.startswith("https://open.spotify.com/track/"):
            raise(NotAValidThemeUrlError(theme_url))
