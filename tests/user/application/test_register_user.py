# import pytest
# from faker import Faker
# from typing import List

# from tests.user.infrastructure.user_in_memory_repository import UserInMemoryRepository
# from tests.user.builder.user_builder import UserBuilder
# from src.user.application.register_user import RegisterUser
# from src.user.domain.soundtrack_id import SoundtrackId
# from src.user.domain.user_id import UserId
# from src.user.domain.user import User
# from src.user.domain.already_existing_user_error import AlreadyExistingUserError

# fake = Faker()


# user_repository = UserInMemoryRepository()
# use_case: RegisterUser = RegisterUser(user_repository)

# user_id: UserId = UserId.from_string(fake.pystr())
# favorites: List[SoundtrackId] = []
# likes: List[SoundtrackId] = []
# soundtracks: List[SoundtrackId] = []
# following: List[UserId] = []
# followers: List[UserId] = []


# class TestRegisterUser():

#     def test_new_user_is_registered(self):
#         user: User = UserBuilder().with_user_id(user_id).with_favorites(favorites).with_likes(
#             likes).with_soundtracks(soundtracks).with_following(following).with_followers(followers).build()

#         use_case.run(user)

#         found_user = user_repository.find(user_id)
#         assert found_user.user_id.value == user_id.value
#         assert found_user.favorites == favorites
#         assert found_user.likes == likes
#         assert found_user.soundtracks == soundtracks
#         assert found_user.following == following
#         assert found_user.followers == followers

#     def test_already_existing_user_throws_an_error(self):
#         user: User = UserBuilder().with_user_id(user_id).with_favorites(favorites).with_likes(
#             likes).with_soundtracks(soundtracks).with_following(following).with_followers(followers).build()

#         with pytest.raises(AlreadyExistingUserError):
#             use_case.run(user)
