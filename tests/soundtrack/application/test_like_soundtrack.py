from typing import List
import pytest
import uuid

from src.soundtrack.application.like_soundtrack import LikeSoundtrack
from src.soundtrack.domain.exceptions.already_liked_soundtrack_error import AlreadyLikedSoundtrackError
from src.soundtrack.domain.soundtrack_id import SoundtrackId
from src.soundtrack.domain.user_id import UserId
from ..infrastructure.soundtrack_in_memory_repository import SoundtrackInMemoryRepository
from ..builder.soundtrack_builder import SoundtrackBuilder

soundtrack_repository = SoundtrackInMemoryRepository()
use_case: LikeSoundtrack = LikeSoundtrack(soundtrack_repository)


class TestLikeSoundtrack():

    def test_soundtrack_is_liked(self):
        user_id = UserId.from_string(str(uuid.uuid4()))
        soundtrack = SoundtrackBuilder().build()
        soundtrack_repository.save(soundtrack)
        
        use_case.run(user_id, soundtrack.soundtrack_id)

        found_likes: List[UserId] = soundtrack_repository.get_likes(
            soundtrack.soundtrack_id)
        assert found_likes != None
        assert len(found_likes) == 1
        assert found_likes[0].value == user_id.value

    def test_already_existing_like_throws_an_error(self):
        user_id = UserId.from_string(str(uuid.uuid4()))
        soundtrack = SoundtrackBuilder().build()
        soundtrack_repository.save(soundtrack)

        soundtrack_repository.save_like(user_id, soundtrack.soundtrack_id)

        with pytest.raises(AlreadyLikedSoundtrackError):
            use_case.run(user_id, soundtrack.soundtrack_id)
