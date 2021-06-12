import pytest
import uuid
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
        soundtrack_id: SoundtrackId = SoundtrackId.from_string(
            str(uuid.uuid4()))
        book: Isbn13 = Isbn13.from_string("978-2-1550-9533-9")
        soundtrack_title: SoundtrackTitle = SoundtrackTitle.from_string(
            fake.pystr())
        author: UserId = UserId.from_string(fake.pystr())
        chapter1: Chapter = Chapter(
            str(uuid.uuid4()), 1, "https: // open.spotify.com/track/" + fake.pystr(), "")
        chapter2: Chapter = Chapter(
            str(uuid.uuid4()), 2, "https: // open.spotify.com/track/" + fake.pystr(), "")
        chapters: list[Chapter] = [chapter1, chapter2]

        soundtrack = Soundtrack(soundtrack_id, book,
                                soundtrack_title, author, chapters)

        assert soundtrack.soundtrack_id.value == soundtrack_id.value
        assert soundtrack.book.value == book.value
        assert soundtrack.soundtrack_title.value == soundtrack_title.value
        assert soundtrack.author.value == author.value
        assert soundtrack.chapters == chapters
