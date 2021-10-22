class Theme():

    def __init__(self, theme: str):
        self.__value: str = theme

    @staticmethod
    def from_string(theme_str: str):
        return Theme(theme_str)

    @property
    def value(self):
        return self.__value

