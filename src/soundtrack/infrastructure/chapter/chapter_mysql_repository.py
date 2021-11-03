import os
import sqlalchemy as db
from typing import Optional, List

from ...domain.chapter.chapter_repository import ChapterRepository
from ...domain.chapter.chapter import Chapter
from ...domain.chapter.chapter_id import ChapterId
from ...domain.soundtrack_id import SoundtrackId
from ...domain.chapter.chapter_number import ChapterNumber
from ...domain.chapter.theme import Theme
from ...domain.chapter.chapter_title import ChapterTitle
from ...domain.soundtrack import Soundtrack


class ChapterMysqlRepository(ChapterRepository):

    def __init__(self):
        self.__db_engine = db.create_engine(os.getenv('DB_ENGINE'))
        self.__db_connection = self.__db_engine.connect()
        self.__db_metadata = db.MetaData()
        self.__chapter = db.Table(
            "chapter", self.__db_metadata, autoload=True, autoload_with=self.__db_engine)


    def save(self, chapter: Chapter):
        query = db.insert(self.__chapter).values(
            chapter_id=chapter.chapter_id.value,
            soundtrack_id=chapter.soundtrack_id.value,
            chapter_number=chapter.chapter_number.value,
            theme=chapter.theme.value,
            chapter_title=chapter.chapter_title.value
        )
        self.__db_connection.execute(query)


    def find(self, chapter_id: ChapterId) -> Optional[Chapter]:
        query = db.select([self.__chapter]).where(
            self.__chapter.columns.chapter_id == chapter_id.value)
        resultProxy = self.__db_connection.execute(query)

        resultSet = resultProxy.fetchall()
        if not resultSet:
            return None

        return self.__getChapterFromResult(resultSet[0])
    

    def find_by_soundtrack(self, soundtrack_id: SoundtrackId) -> List[Chapter]:
        query = db.select([self.__chapter]).where(
            self.__chapter.columns.soundtrack_id == soundtrack_id.value)
        resultProxy = self.__db_connection.execute(query)

        resultSet = resultProxy.fetchall()
        if not resultSet:
            return []

        return self.__getChaptersListFromResult(resultSet)


    def delete(self, chapter_id: ChapterId):
        query = db.delete(self.__chapter
        ).where(self.__chapter.columns.chapter_id == chapter_id.value)
        self.__db_connection.execute(query)


    def clean(self):
        query = db.delete(self.__chapter)
        self.__db_connection.execute(query)


    def __getChapterFromResult(self, result: tuple) -> Soundtrack:
        return Chapter(
            chapter_id=ChapterId.from_string(result[0]),
            soundtrack_id=SoundtrackId.from_string(result[1]),
            chapter_number=ChapterNumber.from_integer(result[2]),
            theme=Theme.from_string(result[3]),
            chapter_title=ChapterTitle.from_string(result[4])
        )

    def __getChaptersListFromResult(self, resultSet: [tuple]) -> List[Chapter]:
        chapters_list: List[Chapter] = []

        for result in resultSet:
            chapter = self.__getChapterFromResult(result)
            chapters_list.append(chapter)

        return chapters_list