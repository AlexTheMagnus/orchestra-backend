from .chapter_id import ChapterId
from ..soundtrack_id import SoundtrackId
from .chapter_title import ChapterTitle
from .chapter_number import ChapterNumber
from .theme import Theme


class Chapter:

    def __init__(self, chapter_id: ChapterId, soundtrack_id: SoundtrackId, 
                chapter_number: ChapterNumber, theme: Theme, chapter_title: ChapterTitle):
        self.__chapter_id: ChapterId = chapter_id
        self.__soundtrack_id: SoundtrackId = soundtrack_id
        self.__chapter_number: ChapterNumber = chapter_number
        self.__theme: Theme = theme
        self.__chapter_title: ChapterTitle = chapter_title

    @property
    def chapter_id(self):
        return self.__chapter_id

    @property
    def soundtrack_id(self):
        return self.__soundtrack_id

    @property
    def chapter_number(self):
        return self.__chapter_number

    @property
    def theme(self):
        return self.__theme

    @property
    def chapter_title(self):
        return self.__chapter_title
