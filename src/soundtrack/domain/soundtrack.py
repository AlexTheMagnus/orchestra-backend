from typing import List

from .soundtrack_id import SoundtrackId
from .isbn_13 import Isbn13
from .soundtrack_title import SoundtrackTitle
from .user_id import UserId
from .chapter.chapter import Chapter


class Soundtrack():

    def __init__(self, soundtrack_id: SoundtrackId, book: Isbn13, soundtrack_title: SoundtrackTitle,
                 author: UserId, chapters: List[Chapter]):
        self.__soundtrack_id: SoundtrackId = soundtrack_id
        self.__book: Isbn13 = book
        self.__soundtrack_title = soundtrack_title
        self.__author: UserId = author
        self.__chapters: List[Chapter] = chapters

    @property
    def soundtrack_id(self):
        return self.__soundtrack_id

    @property
    def book(self):
        return self.__book

    @property
    def soundtrack_title(self):
        return self.__soundtrack_title

    @property
    def author(self):
        return self.__author

    @property
    def chapters(self):
        return self.__chapters
