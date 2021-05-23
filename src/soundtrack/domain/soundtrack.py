from src.soundtrack.domain.soundtrack_id import SoundtrackId
from src.soundtrack.domain.isbn_13 import Isbn13
from src.soundtrack.domain.soundtrack_title import SoundtrackTitle
from src.soundtrack.domain.user_id import UserId
from src.soundtrack.domain.chapter.chapter import Chapter


class Soundtrack():

    def __init__(self, soundtrack_id: SoundtrackId, book: Isbn13,
                 author: UserId, chapters: list[Chapter]):
        self.__soundtrack_id: SoundtrackId = soundtrack_id
        self.__book: Isbn13 = book
        self.__author: UserId = author
        self.__chapters: list[Chapter] = chapters

    @property
    def soundtrack_id(self):
        return self.__soundtrack_id

    @property
    def book(self):
        return self.__book

    @property
    def author(self):
        return self.__author

    @property
    def chapters(self):
        return self.__chapters
