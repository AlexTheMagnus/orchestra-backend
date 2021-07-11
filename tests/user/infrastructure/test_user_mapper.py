# from src.user.domain.user import User
# from src.user.infrastructure.user_dto import UserDTO
# from src.user.infrastructure.user_mapper import UserMapper


# class TestUserMapper:

#     def test_user_aggregate_from_user_dto_has_same_attributes(self):
#         user_id: UserId = UserId.from_string(fake.pystr())
#         email = Email.from_string(fake.email())
#         username = Username.from_string(fake.name())
#         avatar = Avatar.from_url("https://" + fake.pystr())
#         user = User(user_id, email, username, avatar)

#         user_dto: UserDTO = UserBuilder().build_dto()

#         user: User = UserMapper().from_dto_to_aggregate(user_dto)

#         assert user_dto['user_id'] == user.user_id.value
#         assert user_dto['email'] == user.email.value
#         assert user_dto['username'] == user.username.value
#         assert user_dto['avatar'] == user.avatar.value

#     def test_user_dto_from_user_aggregate_has_same_attributes(self):
#         user: User = UserBuilder().build()

#         user_dto: UserDTO = UserMapper().from_aggregate_to_dto(user)

#         assert user_dto['user_id'] == user.user_id.value
#         assert user_dto['email'] == user.email.value
#         assert user_dto['username'] == user.username.value
#         assert user_dto['avatar'] == user.avatar.value
