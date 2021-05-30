import uuid
from faker import Faker

from src.soundtrack.domain.chapter.chapter_id import ChapterId
from src.soundtrack.domain.chapter.chapter_number import ChapterNumber
from src.soundtrack.domain.chapter.theme import Theme
from src.soundtrack.domain.chapter.chapter_title import ChapterTitle
from src.soundtrack.domain.chapter.chapter import Chapter
from src.soundtrack.infrastructure.chapter.chapter_mapper import ChapterMapper
from src.soundtrack.infrastructure.chapter.chapter_dto import ChapterDTO


fake = Faker()


class ChapterBuilder():
    def __init__(self):
        self.__chapter_id: ChapterId = ChapterId.from_string(
            str(uuid.uuid4()))
        self.__chapter_number: ChapterNumber = ChapterNumber.from_integer(
            fake.random_number(2))
        self.__theme: Theme = Theme.from_url(
            "https://open.spotify.com/track/" + fake.pystr())
        self.__chapter_title: ChapterTitle = ChapterTitle.from_string(
            fake.pystr())

    def build(self) -> Chapter:
        return Chapter(
            self.__chapter_id,
            self.__chapter_number,
            self.__theme,
            self.__chapter_title
        )

    def build_dto(self) -> ChapterDTO:
        chapter = self.build()
        return ChapterMapper().from_aggregate_to_dto(chapter)
