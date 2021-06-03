import uuid
from faker import Faker

# from src.soundtrack.infrastructure.soundtrack_mysql_repository import UserMysqlRepository
from src.soundtrack.infrastructure.soundtrack_mapper import SoundtrackMapper
from src.soundtrack.domain.soundtrack_id import SoundtrackId
from src.soundtrack.domain.isbn_13 import Isbn13
from src.soundtrack.domain.user_id import UserId
from src.soundtrack.domain.chapter.chapter import Chapter
from src.soundtrack.domain.soundtrack import Soundtrack
from src.soundtrack.infrastructure.soundtrack_dto import SoundtrackDTO

fake = Faker()


class SoundtrackBuilder():
    def __init__(self):
        self.__soundtrack_id: SoundtrackId = SoundtrackId.from_string(
            str(uuid.uuid4()))
        self.__book: Isbn13 = Isbn13.from_string("978-2-1550-9533-9")
        self.__author: UserId = UserId.from_string(fake.pystr())
        self.__chapters: list[Chapter] = []

    def with_soundtrack_id(self, soundtrack_id: SoundtrackId):
        self.__soundtrack_id = soundtrack_id
        return self

    def with_book(self, book: Isbn13):
        self.__book = book
        return self

    def with_author(self, author: UserId):
        self.__author = author
        return self

    def with_chapters(self, chapters: list[Chapter]):
        self.__chapters = chapters
        return self

    # TODO: implement (if needed) or remove it
    # def insert(self) -> Soundtrack:
    #     soundtrack = self.build()
    #     soundtrack_repository = SoundtrackMysqlRepository()
    #     soundtrack_repository.save(soundtrack)
    #     return soundtrack

    def build(self) -> Soundtrack:
        return Soundtrack(
            self.__soundtrack_id,
            self.__book,
            self.__author,
            self.__chapters
        )

    def build_dto(self) -> SoundtrackDTO:
        soundtrack = self.build()
        return SoundtrackMapper().from_aggregate_to_dto(soundtrack)
