from faker import Faker
from typing import List

from src.user.infrastructure.user_mysql_repository import UserMysqlRepository
from src.user.infrastructure.user_mapper import UserMapper
from src.user.domain.user_id import UserId
from src.user.domain.soundtrack_id import SoundtrackId
from src.user.domain.user import User
from src.user.domain.user_repository import UserRepository
from src.user.infrastructure.user_dto import UserDTO

fake = Faker()


class UserBuilder():
    def __init__(self):
        self.__user_id: UserId = fake.pystr()
        self.__favorites: List[SoundtrackId] = []
        self.__likes: List[SoundtrackId] = []

    def with_user_id(self, user_id: UserId):
        self.__user_id = user_id
        return self

    def with_favorites(self, favorites: List[SoundtrackId]):
        self.__favorites = favorites
        return self

    def with_likes(self, likes: List[SoundtrackId]):
        self.__likes = likes
        return self

    def insert(self) -> User:
        user = self.build()
        user_repository = UserMysqlRepository()
        user_repository.save(user)
        return user

    def build(self) -> User:
        return User(
            self.__user_id,
            self.__favorites,
            self.__likes
        )

    def build_dto(self) -> UserDTO:
        user = self.build()
        return UserMapper().from_aggregate_to_dto(user)
