from ...domain.chapter.chapter_id import ChapterId
from ...domain.soundtrack_id import SoundtrackId
from ...domain.chapter.chapter_number import ChapterNumber
from ...domain.chapter.chapter_title import ChapterTitle
from ...domain.chapter.theme import Theme
from ...domain.chapter.chapter import Chapter
from ...infrastructure.chapter.chapter_dto import ChapterDTO


class ChapterMapper:
    @staticmethod
    def from_dto_to_aggregate(chapter_dto: ChapterDTO) -> Chapter:
        return Chapter(
            chapter_id=ChapterId.from_string(
                chapter_dto['chapter_id']),
            soundtrack_id=SoundtrackId.from_string(
                chapter_dto['soundtrack_id']),
            chapter_number=ChapterNumber.from_integer(
                chapter_dto['chapter_number']),
            theme=Theme.from_string(chapter_dto['theme']),
            chapter_title=ChapterTitle.from_string(
                chapter_dto['chapter_title'])
        )

    @staticmethod
    def from_aggregate_to_dto(chapter: Chapter) -> ChapterDTO:
        return ChapterDTO(
            chapter_id=chapter.chapter_id.value,
            soundtrack_id=chapter.soundtrack_id.value,
            chapter_number=chapter.chapter_number.value,
            theme=chapter.theme.value,
            chapter_title=chapter.chapter_title.value
        )
