from faker import Faker
from typing import List
import uuid

from ...soundtrack.builder.soundtrack_builder import SoundtrackBuilder
from ...soundtrack.infrastructure.soundtrack_in_memory_repository import SoundtrackInMemoryRepository
from ..builder.user_builder import UserBuilder
from ..infrastructure.user_in_memory_repository import UserInMemoryRepository
from src.soundtrack.domain.soundtrack import Soundtrack
from src.user.application.get_user_favorites import GetUserFavorites
from src.user.domain.soundtrack_id import SoundtrackId
from src.user.domain.user import User

fake = Faker()

user_repository = UserInMemoryRepository()
soundtrack_repository = SoundtrackInMemoryRepository()
use_case = GetUserFavorites(user_repository)


class TestGetUserFavorites():
    def test_user_favorites_are_getted(self):
        user: User = UserBuilder().build()
        user_repository.save(user)
        favorites_list: List[SoundtrackId] = []

        for x in range(fake.random_number(1)):
            soundtrack: Soundtrack = SoundtrackBuilder().build()
            soundtrack_repository.save(soundtrack)
            user_repository.save_favorite(user.user_id, soundtrack.soundtrack_id)
            favorites_list.append(soundtrack.soundtrack_id.value)

        str_found_favorites: List[SoundtrackId] = use_case.run(user.user_id)

        assert len(str_found_favorites) == len(favorites_list)
        str_found_favorites = [favorite.value for favorite in str_found_favorites]
        assert set(str_found_favorites) == set(favorites_list)


    def test_user_without_favorites_returns_no_favorites(self):
        user: User = UserBuilder().build()
        user_repository.save(user)

        favorite_soundtracks: List[SoundtrackId] = use_case.run(user.user_id)
        assert len(favorite_soundtracks) == 0

    def test_unexisting_user_returns_no_favorites(self):
        user: User = UserBuilder().build()

        favorite_soundtracks: List[SoundtrackId] = use_case.run(user.user_id)
        assert len(favorite_soundtracks) == 0