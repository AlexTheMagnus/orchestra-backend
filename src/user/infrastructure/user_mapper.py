from src.user.domain.user import User
from src.user.domain.user_id import UserId
from src.user.domain.soundtrack_id import SoundtrackId
from src.user.infrastructure.user_dto import UserDTO


class UserMapper:
    @staticmethod
    def from_dto_to_aggregate(user_dto: UserDTO) -> User:
        favorites_agreggate = [
            SoundtrackId.from_string(x) for x in user_dto['favorites']]

        return User(
            user_id=UserId.from_string(user_dto['user_id']),
            favorites=[
                SoundtrackId.from_string(x) for x in user_dto['favorites']],
            likes=[
                SoundtrackId.from_string(x) for x in user_dto['likes']]
        )

    @staticmethod
    def from_aggregate_to_dto(user: User) -> UserDTO:
        return UserDTO(
            user_id=user.user_id.value,
            favorites=[str(x) for x in user.favorites],
            likes=[str(x) for x in user.likes],
        )
