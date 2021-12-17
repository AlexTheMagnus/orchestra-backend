import pytest
import uuid

from ...soundtrack.builder.soundtrack_builder import SoundtrackBuilder
from ...soundtrack.infrastructure.soundtrack_in_memory_repository import SoundtrackInMemoryRepository
from ..builder.user_builder import UserBuilder
from ..infrastructure.soundtrack_in_memory_reporter import SoundtrackInMemoryReporter
from ..infrastructure.user_in_memory_repository import UserInMemoryRepository
from src.user.application.add_soundtrack_to_favorites import AddSoundtrackToFavorites
from src.user.domain.exceptions.soundtrack_already_added_to_favorites_error import SoundtrackAlreadyAddedToFavoritesError
from src.user.domain.exceptions.unexisting_soundtrack_error import UnexistingSoundtrackError
from src.user.domain.exceptions.unexisting_user_error import UnexistingUserError
from src.user.domain.soundtrack_id import SoundtrackId
from src.user.domain.user_id import UserId

user_repository = UserInMemoryRepository()
soundtrack_repository = SoundtrackInMemoryRepository()
soundtrack_reporter = SoundtrackInMemoryReporter(soundtrack_repository)
use_case = AddSoundtrackToFavorites(user_repository, soundtrack_reporter)

class TestAddSoundtrackToFavorites():

    def test_soundtrack_is_added_to_favorites(self):
        user = UserBuilder().build()
        user_repository.save(user)
        soundtrack = SoundtrackBuilder().build()
        soundtrack_repository.save(soundtrack)
        
        use_case.run(user.user_id, soundtrack.soundtrack_id)

        found_favorites: List[SoundtrackId] = user_repository.get_favorites(user.user_id)
        assert found_favorites != None
        assert len(found_favorites) == 1
        assert found_favorites[0].value == soundtrack.soundtrack_id.value

    def test_add_soundtrack_to_unexisting_user_favorites_throws_an_error(self):
        user_id = UserId.from_string(str(uuid.uuid4()))
        soundtrack = SoundtrackBuilder().build()
        soundtrack_repository.save(soundtrack)

        with pytest.raises(UnexistingUserError):
            use_case.run(user_id, soundtrack.soundtrack_id)

    def test_add_unexisting_soundtrack_to_favorites_throws_an_error(self):
        user = UserBuilder().build()
        user_repository.save(user)
        soundtrack_id = SoundtrackId.from_string(str(uuid.uuid4()))

        with pytest.raises(UnexistingSoundtrackError):
            use_case.run(user.user_id, soundtrack_id)

    def test_add_soundtrack_to_favorites_twice_throws_an_error(self):
        user = UserBuilder().build()
        user_repository.save(user)
        soundtrack = SoundtrackBuilder().build()
        soundtrack_repository.save(soundtrack)

        user_repository.save_favorite(user.user_id, soundtrack.soundtrack_id)

        with pytest.raises(SoundtrackAlreadyAddedToFavoritesError):
            use_case.run(user.user_id, soundtrack.soundtrack_id)
