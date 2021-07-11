import pytest
from faker import Faker

from src.soundtrack.domain.chapter.chapter_title import ChapterTitle
from src.soundtrack.domain.chapter.exceptions.not_a_valid_chapter_title_error import NotAValidChapterTitleError

fake = Faker()


class TestChapterTitle():

    def test_from_string_constructor(self):
        str_chapter_title = fake.pystr()
        chapter_title = ChapterTitle.from_string(str_chapter_title)
        assert chapter_title.value == str_chapter_title

    def test_building_chapter_title_with_an_extra_spaced_string(self):
        str_chapter_title = "  extraSpacedChapterTitle   "
        chapter_title = ChapterTitle.from_string(str_chapter_title)
        assert chapter_title.value == "extraSpacedChapterTitle"

    def test_building_chapter_title_with_an_empty_string(self):
        empty_chapter_title = ""
        chapter_title = ChapterTitle.from_string(empty_chapter_title)
        assert chapter_title.value == ""

    def test_building_chapter_title_with_string_filled_with_spaces(self):
        empty_chapter_title = "   "
        chapter_title = ChapterTitle.from_string(empty_chapter_title)
        assert chapter_title.value == ""
