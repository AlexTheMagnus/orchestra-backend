from .exceptions.not_a_valid_chapter_title_error import NotAValidChapterTitleError


class ChapterTitle():

    def __init__(self, chapter_title: str):
        self.__value: str = chapter_title

    @staticmethod
    def from_string(chapter_title: str):
        chapter_title = chapter_title.strip()
        return ChapterTitle(chapter_title)

    @property
    def value(self):
        return self.__value
