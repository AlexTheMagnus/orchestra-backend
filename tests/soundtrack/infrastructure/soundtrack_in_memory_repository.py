from typing import List, Optional

from src.soundtrack.domain.soundtrack_repository import SoundtrackRepository
from src.soundtrack.domain.soundtrack import Soundtrack
from src.soundtrack.domain.soundtrack_id import SoundtrackId


class SoundtrackInMemoryRepository(SoundtrackRepository):
    def __init__(self):
        self.__soundtracks: List[Soundtrack] = []

    def save(self, soundtrack: Soundtrack):
        self.__soundtracks.append(soundtrack)

    def find(self, soundtrack_id: SoundtrackId) -> Optional[Soundtrack]:

        for soundtrack in self.__soundtracks:
            if soundtrack.soundtrack_id.value == soundtrack_id.value:
                return soundtrack
        return None
