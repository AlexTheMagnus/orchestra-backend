from src.soundtrack.domain.chapter.chapter_id import ChapterId
from src.soundtrack.domain.chapter.chapter_title import ChapterTitle
from src.soundtrack.domain.chapter.chapter_number import ChapterNumber
from src.soundtrack.domain.chapter.theme import Theme


class Chapter:

    def __init__(self, chapter_id, chapter_number, theme, chapter_title):
        self.__chapter_id: ChapterId = chapter_id
        self.__chapter_number: ChapterNumber = chapter_number
        self.__theme: Theme = theme
        self.__chapter_title: ChapterTitle = chapter_title

    @property
    def chapter_id(self):
        return self.__chapter_id

    @property
    def chapter_number(self):
        return self.__chapter_number

    @property
    def theme(self):
        return self.__theme

    @property
    def chapter_title(self):
        return self.__chapter_title
