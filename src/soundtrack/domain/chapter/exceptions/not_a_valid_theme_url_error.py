class NotAValidThemeUrlError(Exception):
    def __init__(self, theme_url: str):
        self.message = '{0} is not a valid theme url.'.format(theme_url)

    def __str__(self):
        return self.message
