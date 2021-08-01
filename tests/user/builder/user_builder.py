from faker import Faker

from src.user.infrastructure.user_mapper import UserMapper
from src.user.domain.user_id import UserId
from src.user.domain.username import Username
from src.user.domain.user_avatar import UserAvatar
from src.user.domain.user import User
from src.user.infrastructure.user_dto import UserDTO

fake = Faker()


class UserBuilder():
    def __init__(self):
        self.__user_id: UserId = UserId.from_string(fake.pystr())
        self.__username: Username = Username.from_string(fake.name())
        self.__user_avatar: UserAvatar = UserAvatar.from_url("https://" + fake.pystr())

    def with_user_id(self, user_id: UserId):
        self.__user_id = user_id
        return self

    def with_username(self, username: Username):
        self.__username = username
        return self

    def with_user_avatar(self, user_avatar: UserAvatar):
        self.__user_avatar = user_avatar
        return self

    def build(self) -> User:
        return User(
            self.__user_id,
            self.__username,
            self.__user_avatar,
        )

    def build_dto(self) -> UserDTO:
        user = self.build()
        return UserMapper().from_aggregate_to_dto(user)
