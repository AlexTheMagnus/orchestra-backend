import uuid
from typing import List

from ..infrastructure.soundtrack_in_memory_repository import SoundtrackInMemoryRepository
from src.soundtrack.domain.user_id import UserId
from src.soundtrack.domain.soundtrack import Soundtrack
from ..builder.soundtrack_builder import SoundtrackBuilder
from src.soundtrack.application.get_user_soundtracks import GetUserSoundtracks


soundtrack_repository = SoundtrackInMemoryRepository()
use_case: GetUserSoundtracks = GetUserSoundtracks(soundtrack_repository)
author: UserId = UserId.from_string(str(uuid.uuid4()))
author_without_soundtracks: UserId = UserId.from_string(str(uuid.uuid4()))
unexisting_author: UserId = UserId.from_string(str(uuid.uuid4()))

for x in range(4):
    soundtrack: Soundtrack = SoundtrackBuilder().with_author(author).build()
    soundtrack_repository.save(soundtrack)


class TestGetUserSoundtracks():
    def test_user_soundtracks_are_getted(self):
        found_soundtracks: List[Soundtrack] = use_case.run(author)
        assert len(found_soundtracks) == 4

    def test_user_without_soundtracks_returns_no_soundtracks(self):
        found_soundtracks: List[Soundtrack] = use_case.run(author_without_soundtracks)
        assert len(found_soundtracks) == 0

    def test_unexisting_user_returns_no_soundtracks(self):
        found_soundtracks: List[Soundtrack] = use_case.run(unexisting_author)
        assert len(found_soundtracks) == 0