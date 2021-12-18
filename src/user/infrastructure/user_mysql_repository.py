from typing import Optional, List
import os
import sqlalchemy as db

from ..domain.soundtrack_id import SoundtrackId
from ..domain.user import User
from ..domain.user_avatar import UserAvatar
from ..domain.user_id import UserId
from ..domain.user_repository import UserRepository
from ..domain.username import Username

class UserMysqlRepository(UserRepository):

    def __init__(self):
        self.__db_engine = db.create_engine(os.getenv('DB_ENGINE'))
        self.__db_connection = self.__db_engine.connect()
        self.__db_metadata = db.MetaData()
        self.__users = db.Table(
            "user", self.__db_metadata, autoload=True, autoload_with=self.__db_engine)
        self.__favorites = db.Table(
            "favorite", self.__db_metadata, autoload=True, autoload_with=self.__db_engine)
        self.__follows = db.Table(
            "follow", self.__db_metadata, autoload=True, autoload_with=self.__db_engine)


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

        return self.__get_user_from_result(resultSet[0])


    def save_favorite(self, user_id: UserId, soundtrack_id: SoundtrackId):
        query = db.insert(self.__favorites).values(
            user_id=user_id.value, soundtrack_id=soundtrack_id.value
        )
        self.__db_connection.execute(query)


    def get_favorites(self, user_id: UserId) -> List[SoundtrackId]:
        query = db.select([self.__favorites]
        ).where(self.__favorites.columns.user_id == user_id.value)
        resultProxy = self.__db_connection.execute(query)

        resultSet = resultProxy.fetchall()
        if not resultSet:
            return []

        return self.__get_favorite_list_from_result(resultSet)


    def remove_favorite(self, user_id: UserId, soundtrack_id: SoundtrackId):
        query = db.delete(self.__favorites
        ).where(self.__favorites.columns.soundtrack_id == soundtrack_id.value and self.__favorites.columns.user_id == user_id.value)
        self.__db_connection.execute(query)        


    def save_follow(self, follower_id: UserId, followed_id: UserId):
        query = db.insert(self.__follows).values(
            follower=follower_id.value, followed=followed_id.value
        )
        self.__db_connection.execute(query)


    def get_followers(self, user_id: UserId) -> List[User]:
        query = db.select([self.__follows.columns.follower]).where(
            self.__follows.columns.followed == user_id.value)
        resultProxy = self.__db_connection.execute(query)

        followerIdsResultSet = resultProxy.fetchall()
        if not followerIdsResultSet:
            return []

        return [self.find(UserId.from_string(followerIdResult[0])) for followerIdResult in followerIdsResultSet]


    def get_followed_users(self, user_id: UserId) -> List[User]:
        query = db.select([self.__follows.columns.followed]).where(
            self.__follows.columns.follower == user_id.value)
        resultProxy = self.__db_connection.execute(query)

        followedUserIdsResultSet = resultProxy.fetchall()
        if not followedUserIdsResultSet:
            return []

        return [self.find(UserId.from_string(followedUserIdResult[0])) for followedUserIdResult in followedUserIdsResultSet]


    def __get_user_from_result(self, result: tuple) -> User:
        return User(
            user_id=UserId.from_string(result[0]),
            username=Username.from_string(result[1]),
            user_avatar=UserAvatar.from_url(result[2])
        )


    def __get_favorite_list_from_result(self, resultSet: [tuple]) -> List[SoundtrackId]:
        favorites_list: List[SoundtrackId] = []

        for result in resultSet:
            favorite = SoundtrackId.from_string(result[1])
            favorites_list.append(favorite)

        return favorites_list        


    def clean(self):
        query = db.delete(self.__follows)
        self.__db_connection.execute(query)

        query = db.delete(self.__favorites)
        self.__db_connection.execute(query)

        query = db.delete(self.__users)
        self.__db_connection.execute(query)
        