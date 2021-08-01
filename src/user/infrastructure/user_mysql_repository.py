import os
import sqlalchemy as db

from src.user.domain.user_repository import UserRepository
from ..domain.user import User
from ..domain.user_id import UserId
from ..domain.username import Username
from ..domain.user_avatar import UserAvatar

class UserMysqlRepository(UserRepository):

    def __init__(self):
        self.__db_engine = db.create_engine(os.getenv('DB_ENGINE'))
        self.__db_connection = self.__db_engine.connect()
        self.__db_metadata = db.MetaData()
        self.__users = db.Table(
            "user", self.__db_metadata, autoload=True, autoload_with=self.__db_engine)

    def save(self, user: User):
        query = db.insert(self.__users).values(
            user_id=user.user_id.value,
            username=user.username.value,
            user_avatar=user.user_avatar.value
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

    def __getUserFromResult(self, result: tuple) -> User:
        return User(
            user_id=UserId.from_string(result[0]),
            username=Username.from_string(result[1]),
            user_avatar=UserAvatar.from_url(result[2])
        )
