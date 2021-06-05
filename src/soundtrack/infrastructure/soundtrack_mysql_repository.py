import os
import sqlalchemy as db

from src.soundtrack.domain.soundtrack_repository import SoundtrackRepository
from src.soundtrack.domain.soundtrack import Soundtrack
from src.soundtrack.domain.user_id import UserId


class SoundtrackMysqlRepository(SoundtrackRepository):

    def __init__(self):
        self.__db_engine = db.create_engine(os.getenv('DB_ENGINE'))
        self.__db_connection = self.__db_engine.connect()
        self.__db_metadata = db.MetaData()
        self.__soundtrack = db.Table(
            "soundtrack", self.__db_metadata, autoload=True, autoload_with=self.__db_engine)
        self.__chapter = db.Table(
            "chapter", self.__db_metadata, autoload=True, autoload_with=self.__db_engine)

    def save(self, soundtrack: Soundtrack, author_id: UserId):
        query = db.insert(self.__soundtrack).values(
            soundtrack_id=soundtrack.soundtrack_id.value,
            book=soundtrack.book.value,
            soundtrack_title=soundtrack.soundtrack_title.value,
            author=author_id
        )

        # TODO: for each chapter -> query
        query = db.insert(self.__chapter).values(
            chapter_id=author_id,
            soundtrack_id=soundtrack.soundtrack_id.value
            # ...
        )

        self.__db_connection.execute(query)

    def find(self, user_id: UserId) -> Optional[User]:
        query = db.select([self.__users]).where(
            self.__users.columns.user_id == user_id.value)
        resultProxy = self.__db_connection.execute(query)

        resultSet = resultProxy.fetchall()
        if not resultSet:
            return None

        return self.__getUserFromResult(resultSet[0])
