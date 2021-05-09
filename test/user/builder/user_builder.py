from faker import Faker

from src.user.infrastructure.user_mysql_repository import UserMysqlRepository
from src.user.infrastructure.user_mapper import UserMapper
from src.user.domain.user_id import UserId
from src.user.domain.email import Email
from src.user.domain.username import Username
from src.user.domain.avatar import Avatar
from src.user.domain.user import User
from src.user.domain.user_repository import UserRepository


class UserBuilder():
    def __init__(self):
        self.__user_id: UserId = fake.pystr()
        self.__email: Email = fake.email()
        self.__username: Username = fake.name()
        self.__avatar: Avatar = "https://" + fake.pystr()

    def with_user_id(self, user_id: UserId):
        self.__user_id = user_id
        return self

    def with_email(self, email: str):
        self.__email = email
        return self

    def with_username(self, username: str):
        self.__username = username
        return self

    def with_avatar(self, avatar: str):
        self.__avatar = avatar
        return self

    def insert(self) -> User:
        user = self.build()
        user_repository = UserMysqlRepository()
        user_repository.save(user)
        return user

    def build(self) -> User:
        return User(
            self.__user_id,
            self.__email,
            self.__username,
            self.__avatar
        )

    def build_dto(self) -> UserDTO:
        user = self.build()
        return UserMapper().from_aggregate_to_dto(user)
