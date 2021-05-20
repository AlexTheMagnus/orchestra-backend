import pytest
import uuid
from faker import Faker

from src.soundtrack.domain.chapter.chapter_id import ChapterId
from src.soundtrack.domain.chapter.chapter_title import ChapterTitle
from src.soundtrack.domain.chapter.chapter_number import ChapterNumber
from src.soundtrack.domain.chapter.theme import Theme
from src.soundtrack.domain.chapter import Chapter

fake = Faker()


class TestChapter():

    def test_chapter_creation(self):
        chapter_id = ChapterId.from_string(str(uuid.uuid4()))
        chapter_title = ChapterTitle.from_string(fake.pystr())
        chapter_number = ChapterNumber.from_integer(fake.random_number(2))
        chapter_title = ""
