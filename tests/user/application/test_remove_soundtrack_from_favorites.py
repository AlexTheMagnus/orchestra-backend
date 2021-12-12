import pytest
import uuid

from ...soundtrack.builder import soundtrack_builder
from ...soundtrack.builder.soundtrack_builder import SoundtrackBuilder
from ...soundtrack.infrastructure.soundtrack_in_memory_repository import SoundtrackInMemoryRepository
from ..builder.user_builder import UserBuilder
from ..infrastructure.user_in_memory_repository import UserInMemoryRepository
from src.user.application.remove_soundtrack_from_favorites import RemoveSoundtrackFromFavorites
from src.user.domain.exceptions.unexisting_favorite_error import UnexistingFavoriteError
from src.user.domain.soundtrack_id import SoundtrackId
from src.user.domain.user import User
from src.user.domain.user_id import UserId 

user_repository = UserInMemoryRepository()
soundtrack_repository = SoundtrackInMemoryRepository()
use_case: RemoveSoundtrackFromFavorites = RemoveSoundtrackFromFavorites(user_repository)

class TestRemoveSoundtrackFromFavorites():
    def test_soundtrack_is_removed_from_favorites(self):
        user = UserBuilder().build()
        user_repository.save(user)
        soundtrack_to_be_removed = SoundtrackBuilder().build()
        soundtrack_to_be_kept = SoundtrackBuilder().build()
        soundtrack_repository.save(soundtrack_to_be_kept)
        soundtrack_repository.save(soundtrack_to_be_removed)
        user_repository.save_favorite(user.user_id, soundtrack_to_be_removed.soundtrack_id)
        user_repository.save_favorite(user.user_id, soundtrack_to_be_kept.soundtrack_id)

        use_case.run(user.user_id, soundtrack_to_be_removed.soundtrack_id)

        saved_favorites: List[SoundtrackId] = user_repository.get_favorites(user.user_id)
        assert len(saved_favorites) == 1
        assert saved_favorites[0].value ==soundtrack_to_be_kept.soundtrack_id.value

    def test_removing_an_unexisting_favorite_raises_an_error(self):
        user_id = UserId.from_string(str(uuid.uuid4()))
        soundtrack_id = SoundtrackId.from_string(str(uuid.uuid4()))

        with pytest.raises(UnexistingFavoriteError):
            use_case.run(user_id, soundtrack_id)