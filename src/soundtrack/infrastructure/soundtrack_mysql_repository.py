import os
import sqlalchemy as db
from typing import List, Optional

from ..domain.soundtrack_repository import SoundtrackRepository
from ..domain.soundtrack import Soundtrack
from ..domain.soundtrack_id import SoundtrackId
from ..domain.isbn_13 import Isbn13
from ..domain.soundtrack_title import SoundtrackTitle
from ..domain.user_id import UserId
from ..domain.chapter.chapter import Chapter


class SoundtrackMysqlRepository(SoundtrackRepository):

    def __init__(self):
        self.__db_engine = db.create_engine(os.getenv('DB_ENGINE'))
        self.__db_connection = self.__db_engine.connect()
        self.__db_metadata = db.MetaData()
        self.__soundtrack = db.Table(
            "soundtrack", self.__db_metadata, autoload=True, autoload_with=self.__db_engine)
        self.__likes = db.Table(
            "likes", self.__db_metadata, autoload=True, autoload_with=self.__db_engine)


    def save(self, soundtrack: Soundtrack):
        query = db.insert(self.__soundtrack).values(
            soundtrack_id=soundtrack.soundtrack_id.value,
            book=soundtrack.book.value,
            soundtrack_title=soundtrack.soundtrack_title.value,
            author=soundtrack.author.value
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


    def find_by_author(self, author: UserId) -> List[Soundtrack]:
        query = db.select([self.__soundtrack]).where(
            self.__soundtrack.columns.author == author.value)
        resultProxy = self.__db_connection.execute(query)

        resultSet = resultProxy.fetchall()
        if not resultSet:
            return []

        return self.__getSoundtracksListFromResult(resultSet)


    def update(self, soundtrack_to_update: Soundtrack):
        query = db.update(self.__soundtrack).values(
            soundtrack_id=soundtrack_to_update.soundtrack_id.value,
            book=soundtrack_to_update.book.value,
            soundtrack_title=soundtrack_to_update.soundtrack_title.value,
            author=soundtrack_to_update.author.value
        ).where(self.__soundtrack.columns.soundtrack_id == soundtrack_to_update.soundtrack_id.value)

        self.__db_connection.execute(query)


    def delete(self, soundtrack_id: SoundtrackId):
        query = db.delete(self.__soundtrack
        ).where(self.__soundtrack.columns.soundtrack_id == soundtrack_id.value)
        self.__db_connection.execute(query)


    def save_like(self, user_id: UserId, soundtrack_id: SoundtrackId):
        query = db.insert(self.__likes).values(
            user_id=user_id.value,
            soundtrack_id=soundtrack_id.value
        )
        self.__db_connection.execute(query)


    def get_likes(self, soundtrack_id: SoundtrackId) -> List[UserId]:
        query = db.select([self.__likes]
        ).where(self.__likes.columns.soundtrack_id == soundtrack_id.value)
        resultProxy = self.__db_connection.execute(query)

        resultSet = resultProxy.fetchall()
        if not resultSet:
            return []

        return self.__getLikesListFromResult(resultSet)


    def clean(self):
        query = db.delete(self.__soundtrack)
        self.__db_connection.execute(query)


    def __getSoundtrackFromResult(self, result: tuple) -> Soundtrack:
        return Soundtrack(
            soundtrack_id=SoundtrackId.from_string(result[0]),
            book=Isbn13.from_string(result[1]),
            soundtrack_title=SoundtrackTitle.from_string(result[2]),
            author=UserId.from_string(result[3]),
            chapters=[]
        )


    def __getSoundtracksListFromResult(self, resultSet: [tuple]) -> List[Soundtrack]:
        soundtracks_list: List[Soundtrack] = []

        for result in resultSet:
            soundtrack = self.__getSoundtrackFromResult(result)
            soundtracks_list.append(soundtrack)

        return soundtracks_list

    
    def __getLikesListFromResult(self, resultSet: [tuple]) -> List[UserId]:
        likes_list: List[UserId] = []

        for result in resultSet:
            like = UserId.from_string(result[0])
            likes_list.append(like)

        return likes_list