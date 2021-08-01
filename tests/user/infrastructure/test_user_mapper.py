from src.user.domain.user_id import UserId
from src.user.domain.username import Username
from src.user.domain.user_avatar import UserAvatar
from src.user.domain.user import User
from src.user.infrastructure.user_dto import UserDTO
from src.user.infrastructure.user_mapper import UserMapper
from ..builder.user_builder import UserBuilder


class TestUserMapper:

    def test_user_aggregate_from_user_dto_has_same_attributes(self):
        user_dto: UserDTO = UserBuilder().build_dto()

        user: User = UserMapper().from_dto_to_aggregate(user_dto)

        assert user_dto['user_id'] == user.user_id.value
        assert user_dto['username'] == user.username.value
        assert user_dto['user_avatar'] == user.user_avatar.value

    def test_user_dto_from_user_aggregate_has_same_attributes(self):
        user: User = UserBuilder().build()

        user_dto: UserDTO = UserMapper().from_aggregate_to_dto(user)

        assert user_dto['user_id'] == user.user_id.value
        assert user_dto['username'] == user.username.value
        assert user_dto['user_avatar'] == user.user_avatar.value
