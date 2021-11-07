from typing import List
import pytest
import uuid

from src.soundtrack.application.unlike_soundtrack import UnlikeSoundtrack
from src.soundtrack.domain.soundtrack import Soundtrack
from src.soundtrack.domain.user_id import UserId
from src.soundtrack.domain.exceptions.unexisting_like_error import UnexistingLikeError
from ..builder.soundtrack_builder import SoundtrackBuilder
from ..infrastructure.soundtrack_in_memory_repository import SoundtrackInMemoryRepository

soundtrack_repository = SoundtrackInMemoryRepository()
use_case: UnlikeSoundtrack = UnlikeSoundtrack(soundtrack_repository)

class TestUnlikeSoundtrack():
    def test_soundtrack_is_unliked(self):
        user_who_unlike = UserId.from_string(str(uuid.uuid4()))
        user_who_keep_the_like = UserId.from_string(str(uuid.uuid4()))
        soundtrack: Soundtrack = SoundtrackBuilder().build()
        soundtrack_repository.save(soundtrack)
        soundtrack_repository.save_like(user_who_unlike, soundtrack.soundtrack_id)
        soundtrack_repository.save_like(user_who_keep_the_like, soundtrack.soundtrack_id)

        use_case.run(user_who_unlike, soundtrack.soundtrack_id)

        saved_likes: List[UserId] = soundtrack_repository.get_likes(soundtrack.soundtrack_id)
        assert len(saved_likes) == 1
        assert saved_likes[0].value ==user_who_keep_the_like.value

    def test_unexisting_like_raises_an_error(self):
        user_id = UserId.from_string(str(uuid.uuid4()))
        soundtrack: Soundtrack = SoundtrackBuilder().build()
        soundtrack_repository.save(soundtrack)

        with pytest.raises(UnexistingLikeError):
            use_case.run(user_id, soundtrack.soundtrack_id)