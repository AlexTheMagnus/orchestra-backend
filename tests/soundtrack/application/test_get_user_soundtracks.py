import uuid
from faker import Faker
from typing import List

from ..infrastructure.soundtrack_in_memory_repository import SoundtrackInMemoryRepository
from src.soundtrack.domain.user_id import UserId
from src.soundtrack.domain.soundtrack import Soundtrack
from ..builder.soundtrack_builder import SoundtrackBuilder
from src.soundtrack.application.get_user_soundtracks import GetUserSoundtracks

fake = Faker()

soundtrack_repository = SoundtrackInMemoryRepository()
use_case: GetUserSoundtracks = GetUserSoundtracks(soundtrack_repository)
author: UserId = UserId.from_string(fake.pystr())
author_without_soundtracks: UserId = UserId.from_string(fake.pystr())

for x in range(4):
    soundtrack: Soundtrack = SoundtrackBuilder().with_author(author).build()
    soundtrack_repository.save(soundtrack)


class TestGetUserSoundtracks():
    def test_user_soundtracks_are_getted(self):
        found_soundtracks: List[Soundtrack] = use_case.run(author)
        assert len(found_soundtracks) == 4

    def test_user_without_soundtracks_return_no_soundtracks(self):
        found_soundtracks: List[Soundtrack] = use_case.run(author_without_soundtracks)
        assert len(found_soundtracks) == 0