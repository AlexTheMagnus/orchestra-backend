import pytest
from faker import Faker

from src.soundtrack.domain.soundtrack_id import SoundtrackId
from src.soundtrack.domain.isbn_13 import Isbn13
from src.soundtrack.domain.soundtrack_title import SoundtrackTitle
from src.soundtrack.domain.user_id import UserId
from src.soundtrack.domain.chapter.chapter import Chapter
from src.soundtrack.domain.soundtrack import Soundtrack

fake = Faker()


class TestSoundtrack():

    def test_soundtrack_constructor(self):
        soundtrack_id: SoundtrackId = SoundtrackId.from_string(fake.pystr())
        book: Isbn13 = Isbn13.from_string("978-2-1550-9533-9")
        author: UserId = UserId.from_string(fake.pystr())
        chapters: list[Chapter] = []

        soundtrack = Soundtrack(soundtrack_id, book, author, chapters)

        assert soundtrack.soundtrack_id.value == soundtrack_id.value
        assert soundtrack.book.value == book.value
        assert soundtrack.author.value == author.value
        assert soundtrack.chapters.value == chapters.value
