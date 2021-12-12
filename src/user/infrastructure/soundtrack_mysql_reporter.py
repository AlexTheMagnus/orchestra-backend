import os
import sqlalchemy as db

from ..domain.soundtrack_reporter import SoundtrackReporter
from ..domain.soundtrack_id import SoundtrackId

class SoundtrackMysqlReporter(SoundtrackReporter):

    def __init__(self):
        self.__db_engine = db.create_engine(os.getenv('DB_ENGINE'))
        self.__db_connection = self.__db_engine.connect()
        self.__db_metadata = db.MetaData()
        self.__soundtrack = db.Table(
            "soundtrack", self.__db_metadata, autoload=True, autoload_with=self.__db_engine)


    def exist(self, soundtrack_id: SoundtrackId) -> bool:
        query = db.select([self.__soundtrack]).where(
            self.__soundtrack.columns.soundtrack_id == soundtrack_id.value)
        resultProxy = self.__db_connection.execute(query)

        resultSet = resultProxy.fetchall()
        if resultSet:
            return True

        return False