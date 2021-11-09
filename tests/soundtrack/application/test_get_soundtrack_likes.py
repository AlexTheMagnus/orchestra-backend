import uuid
from typing import List

from src.soundtrack.application.get_soundtrack_likes import GetSoundtrackLikes
from src.soundtrack.domain.soundtrack import Soundtrack
from src.soundtrack.domain.user_id import UserId
from ..builder.soundtrack_builder import SoundtrackBuilder
from ..infrastructure.soundtrack_in_memory_repository import SoundtrackInMemoryRepository

soundtrack_repository = SoundtrackInMemoryRepository()
use_case = GetSoundtrackLikes(soundtrack_repository)


class TestSoundtrackLikes():
    def test_soundtrack_likes_are_getted(self):
        soundtrack: Soundtrack = SoundtrackBuilder().build()
        soundtrack_repository.save(soundtrack)

        for x in range(2):
          user_id = UserId.from_string(str(uuid.uuid4()))
          soundtrack_repository.save_like(user_id, soundtrack.soundtrack_id)

        likes: List[UserId] = use_case.run(soundtrack.soundtrack_id)
        assert len(likes) == 2

    def test_soundtrack_without_likes_returns_no_likes(self):
        soundtrack: Soundtrack = SoundtrackBuilder().build()
        soundtrack_repository.save(soundtrack)

        likes: List[UserId] = use_case.run(soundtrack.soundtrack_id)
        assert len(likes) == 0

    def test_unexisting_soundtrack_returns_no_likes(self):
        soundtrack: Soundtrack = SoundtrackBuilder().build()

        likes: List[UserId] = use_case.run(soundtrack.soundtrack_id)
        assert len(likes) == 0