import pytest
import uuid
from faker import Faker

from src.soundtrack.domain.chapter.chapter_id import ChapterId
from src.soundtrack.domain.chapter.chapter_title import ChapterTitle
from src.soundtrack.domain.chapter.chapter_number import ChapterNumber
from src.soundtrack.domain.chapter.theme import Theme
from src.soundtrack.domain.chapter.chapter import Chapter

fake = Faker()


class TestChapter():

    def test_chapter_constructor(self):
        chapter_id = ChapterId.from_string(str(uuid.uuid4()))
        chapter_number = ChapterNumber.from_integer(fake.random_number(2))
        theme = Theme.from_url(
            "https://open.spotify.com/track/" + fake.pystr())
        chapter_title = ChapterTitle.from_string(fake.pystr())

        chapter = Chapter(chapter_id, chapter_number, theme, chapter_title)

        assert chapter.chapter_id.value == chapter_id.value
        assert chapter.chapter_number.value == chapter_number.value
        assert chapter.theme.value == theme.value
        assert chapter.chapter_title.value == chapter_title.value
