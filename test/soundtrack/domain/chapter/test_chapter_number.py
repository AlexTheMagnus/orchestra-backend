import pytest
from faker import Faker

from src.soundtrack.domain.chapter.chapter_number import ChapterNumber
from src.soundtrack.domain.chapter.exceptions.not_a_valid_chapter_number_error import NotAValidChapterNumberError

fake = Faker()


class TestChapterNumber():

    def test_from_integer_constructor(self):
        int_chapter_number = 3.5
        chapter_number = ChapterNumber.from_integer(int_chapter_number)
        assert chapter_number.value == int_chapter_number

    def test_building_chapter_number_with_a_negative_number_throws_an_error(self):
        negative_chapter_number = fake.random_number(2) * -1
        with pytest.raises(NotAValidChapterNumberError):
            chapter_number = ChapterNumber.from_integer(
                negative_chapter_number)
