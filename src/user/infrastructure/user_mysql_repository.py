import os
import sqlalchemy as db

from src.domain.user_repository import UserRepository


class UserMysqlRepository(UserRepository):

    def __init__(self):
        self.__db_engine = db.create_engine(os.getenv('DB_ENGINE'))
        self.__db_connection = self.__db_engine.connect()
        self.__db_metadata = db.MetaData()
        self.__users = db.Table(
            "users", self.__db_metadata, autoload=True, autoload_with=self.__db_engine)
