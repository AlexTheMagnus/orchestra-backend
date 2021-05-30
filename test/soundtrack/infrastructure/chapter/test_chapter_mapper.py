from src.soundtrack.domain.chapter.chapter import Chapter
from src.soundtrack.infrastructure.chapter.chapter_mapper import ChapterMapper
from src.soundtrack.infrastructure.chapter.chapter_dto import ChapterDTO
from test.soundtrack.builder.chapter_builder import ChapterBuilder


class TestChapterMapper:

    def test_chapter_aggregate_from_chapter_dto_has_same_attributes(self):
        chapter_dto: ChapterDTO = ChapterBuilder().build_dto()

        chapter: Chapter = ChapterMapper().from_dto_to_aggregate(chapter_dto)

        assert chapter_dto['chapter_id'] == chapter.chapter_id.value
        assert chapter_dto['chapter_number'] == chapter.chapter_number.value
        assert chapter_dto['theme'] == chapter.theme.value
        assert chapter_dto['chapter_title'] == chapter.chapter_title.value

    def test_chapter_dto_from_chapter_aggregate_has_same_attributes(self):
        chapter: Chapter = ChapterBuilder().build()

        chapter_dto: ChapterDTO = ChapterMapper().from_aggregate_to_dto(chapter)

        assert chapter_dto['chapter_id'] == chapter.chapter_id.value
        assert chapter_dto['chapter_number'] == chapter.chapter_number.value
        assert chapter_dto['theme'] == chapter.theme.value
        assert chapter_dto['chapter_title'] == chapter.chapter_title.value
