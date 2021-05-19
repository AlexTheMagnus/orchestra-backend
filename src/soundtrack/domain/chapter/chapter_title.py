from src.soundtrack.domain.chapter.exceptions.not_a_valid_chapter_title_error import NotAValidChapterTitleError


class ChapterTitle():

    def __init__(self, chapter_title: str):
        chapter_title = chapter_title.strip()
        self.__validate_not_an_empty_string(chapter_title)
        self.__value: str = chapter_title

    @staticmethod
    def from_string(chapter_title: str):
        return ChapterTitle(chapter_title)

    @property
    def value(self):
        return self.__value

    def __validate_not_an_empty_string(self, chapter_title: str):
        if chapter_title == "":
            raise(NotAValidChapterTitleError(chapter_title))
