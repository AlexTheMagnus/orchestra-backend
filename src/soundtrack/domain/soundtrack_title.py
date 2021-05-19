from src.soundtrack.domain.exceptions.not_a_valid_soundtrack_title_error import NotAValidSoundtrackTitleError


class SoundtrackTitle():

    def __init__(self, soundtrack_title: str):
        soundtrack_title = soundtrack_title.strip()
        self.__validate_not_an_empty_string(soundtrack_title)
        self.__value: str = soundtrack_title

    @staticmethod
    def from_string(soundtrack_title: str):
        return SoundtrackTitle(soundtrack_title)

    @property
    def value(self):
        return self.__value

    def __validate_not_an_empty_string(self, soundtrack_title: str):
        if soundtrack_title == "":
            raise(NotAValidSoundtrackTitleError(soundtrack_title))
