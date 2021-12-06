import os
import sqlalchemy as db
from typing import List, Optional, TypedDict

from ..domain.chapter.chapter import Chapter
from ..domain.isbn_13 import Isbn13
from ..domain.search_options import SearchOptions
from ..domain.soundtrack import Soundtrack
from ..domain.soundtrack_id import SoundtrackId
from ..domain.soundtrack_repository import SoundtrackRepository
from ..domain.soundtrack_title import SoundtrackTitle
from ..domain.user_id import UserId


class SoundtracksWithLikes(TypedDict):
    soundtrack: Soundtrack
    likes: int


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

        return self.__get_soundtrack_from_result(resultSet[0])


    def find_by_author(self, author: UserId) -> List[Soundtrack]:
        query = db.select([self.__soundtrack]).where(
            self.__soundtrack.columns.author == author.value)
        resultProxy = self.__db_connection.execute(query)

        resultSet = resultProxy.fetchall()
        if not resultSet:
            return []

        return self.__get_soundtracks_list_from_result(resultSet)


    def search(self, search_options: SearchOptions) -> List[Soundtrack]:
        found_soundtracks_with_likes: List[SoundtracksWithLikes] = []

        query = db.select([self.__soundtrack]).where(
            self.__soundtrack.columns.book == search_options['book'].value)
        resultProxy = self.__db_connection.execute(query)
        resultSet = resultProxy.fetchall()

        if not resultSet:
            return []

        for soundtrack in self.__get_soundtracks_list_from_result(resultSet):
            found_soundtracks_with_likes.append({"soundtrack": soundtrack, "likes": len(self.get_likes(soundtrack.soundtrack_id))})

        found_soundtracks_with_likes = sorted(found_soundtracks_with_likes, key=lambda d: d['likes'], reverse=True)
        return [soundtrack_with_likes["soundtrack"] for soundtrack_with_likes in found_soundtracks_with_likes]
        

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

        return self.__get_likes_list_from_result(resultSet)


    def delete_like(self, user_id: UserId, soundtrack_id: SoundtrackId):
        query = db.delete(self.__likes
        ).where(self.__likes.columns.soundtrack_id == soundtrack_id.value and self.__likes.columns.user_id == user_id.value)
        self.__db_connection.execute(query)        


    def clean(self):
        query = db.delete(self.__likes)
        self.__db_connection.execute(query)
        query = db.delete(self.__soundtrack)
        self.__db_connection.execute(query)


    def __get_soundtrack_from_result(self, result: tuple) -> Soundtrack:
        return Soundtrack(
            soundtrack_id=SoundtrackId.from_string(result[0]),
            book=Isbn13.from_string(result[1]),
            soundtrack_title=SoundtrackTitle.from_string(result[2]),
            author=UserId.from_string(result[3]),
            chapters=[]
        )


    def __get_soundtracks_list_from_result(self, resultSet: [tuple]) -> List[Soundtrack]:
        soundtracks_list: List[Soundtrack] = []

        for result in resultSet:
            soundtrack = self.__get_soundtrack_from_result(result)
            soundtracks_list.append(soundtrack)

        return soundtracks_list

    
    def __get_likes_list_from_result(self, resultSet: [tuple]) -> List[UserId]:
        likes_list: List[UserId] = []

        for result in resultSet:
            like = UserId.from_string(result[0])
            likes_list.append(like)

        return likes_list