from src.user.domain.user_id import UserId
from src.user.domain.username import Username
from src.user.domain.user_avatar import UserAvatar
from src.user.domain.user import User
from src.user.infrastructure.user_dto import UserDTO


class UserMapper:
    @staticmethod
    def from_dto_to_aggregate(user_dto: UserDTO) -> User:
        return User(
            user_id=UserId.from_string(user_dto['user_id']),
            username=Username.from_string(user_dto['username']),
            user_avatar=UserAvatar.from_url(user_dto['user_avatar'])
        )

    @staticmethod
    def from_aggregate_to_dto(user: User) -> UserDTO:
        return UserDTO(
            user_id=user.user_id.value,
            username=user.username.value,
            user_avatar=user.user_avatar.value
        )
