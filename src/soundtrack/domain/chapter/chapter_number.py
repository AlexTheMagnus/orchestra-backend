from src.soundtrack.domain.chapter.exceptions.not_a_valid_chapter_number_error import NotAValidChapterNumberError


class ChapterNumber():

    def __init__(self, chapter_number: int):
        self.__validate_not_a_negative_number(chapter_number)
        self.__value: str = chapter_number

    @staticmethod
    def from_integer(chapter_number: int):
        return ChapterNumber(chapter_number)

    @property
    def value(self):
        return self.__value

    def __validate_not_a_negative_number(self, chapter_number: str):
        if chapter_number < 0:
            raise(NotAValidChapterNumberError(chapter_number))
