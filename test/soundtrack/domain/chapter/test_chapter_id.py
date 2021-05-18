import pytest
import uuid

from src.soundtrack.domain.chapter_id import ChapterId
from src.soundtrack.domain.not_a_valid_chapter_id_error import NotAValidChapterIdError


class TestChapterId():

    def test_from_string_constructor(self):
        str_chapter_id = str(uuid.uuid4())
        chapter_id = ChapterId.from_string(str_chapter_id)
        assert chapter_id.value == str_chapter_id

    def test_building_chapter_id_with_a_non_uuid4_throws_an_error(self):
        str_chapter_id = str(uuid.uuid1())
        with pytest.raises(NotAValidChapterIdError):
            chapter_id = ChapterId.from_string(str_chapter_id)
