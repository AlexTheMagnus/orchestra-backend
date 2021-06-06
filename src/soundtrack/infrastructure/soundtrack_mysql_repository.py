import os
import sqlalchemy as db

from src.soundtrack.domain.soundtrack_repository import SoundtrackRepository
from src.soundtrack.domain.soundtrack import Soundtrack
from src.soundtrack.domain.soundtrack_id import SoundtrackId
from src.soundtrack.domain.isbn_13 import Isbn13
from src.soundtrack.domain.soundtrack_title import SoundtrackTitle
from src.soundtrack.domain.user_id import UserId
from src.soundtrack.domain.chapter.chapter import Chapter


class SoundtrackMysqlRepository(SoundtrackRepository):

    def __init__(self):
        self.__db_engine = db.create_engine(os.getenv('DB_ENGINE'))
        self.__db_connection = self.__db_engine.connect()
        self.__db_metadata = db.MetaData()
        self.__soundtrack = db.Table(
            "soundtrack", self.__db_metadata, autoload=True, autoload_with=self.__db_engine)
        self.__chapter = db.Table(
            "chapter", self.__db_metadata, autoload=True, autoload_with=self.__db_engine)

    def save(self, soundtrack: Soundtrack):
        query = db.insert(self.__soundtrack).values(
            soundtrack_id=soundtrack.soundtrack_id.value,
            book=soundtrack.book.value,
            soundtrack_title=soundtrack.soundtrack_title.value,
            author=soundtrack.author.value
        )

        for chapter in soundtrack.chapters:
            query = db.insert(self.__chapter).values(
                chapter_id=chapter.chapter_id.value,
                soundtrack_id=soundtrack.soundtrack_id.value,
                chapter_number=chapter.chapter_number.value,
                theme=chapter.theme.value,
                chapter_title=chapter.chapter_title.value
            )

        self.__db_connection.execute(query)

    def find(self, soundtrack_id: SoundtrackId) -> Optional[Soundtrack]:
        query = db.select([self.__soundtrack]).where(
            self.__soundtrack.columns.soundtrack_id == soundtrack_id.value)
        resultProxy = self.__db_connection.execute(query)

        resultSet = resultProxy.fetchall()
        if not resultSet:
            return None

        return self.__getSoundtrackFromResult(resultSet[0])

    def __getSoundtrackFromResult(self, result: tuple) -> Soundtrack:
        return Soundtrack(
            soundtrack_id=SoundtrackId.from_string(result[0]),
            book=Isbn13.from_string(result[1]),
            soundtrack_title=SoundtrackTitle.from_string(result[2]),
            author=UserId.from_string(result[3]),
            chapters=[]
        )
