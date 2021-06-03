import os
import sqlalchemy as db

from src.soundtrack.domain.soundtrack_repository import SoundtrackRepository
from src.soundtrack.domain.soundtrack_id import SoundtrackId


class SoundtrackMysqlRepository(SoundtrackRepository):

    def __init__(self):
        self.__db_engine = db.create_engine(os.getenv('DB_ENGINE'))
        self.__db_connection = self.__db_engine.connect()
        self.__db_metadata = db.MetaData()
        self.__users = db.Table(
            "users", self.__db_metadata, autoload=True, autoload_with=self.__db_engine)

    def save(self, user: User):
        query = db.insert(self.__users).values(
            user_id=user.user_id.value,
            username=user.username,
            password=user.password.value,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            country=user.country,
            city=user.city
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
