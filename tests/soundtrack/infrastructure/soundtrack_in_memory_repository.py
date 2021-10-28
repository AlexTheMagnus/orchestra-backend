from typing import List, Optional

from src.soundtrack.domain.soundtrack_repository import SoundtrackRepository
from src.soundtrack.domain.soundtrack import Soundtrack
from src.soundtrack.domain.soundtrack_id import SoundtrackId
from src.soundtrack.domain.user_id import UserId

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

    def find_by_author(self, author: UserId) -> Optional[Soundtrack]:
        found_soundtracks: List[Soundtrack] = []

        for soundtrack in self.__soundtracks:
            if soundtrack.author.value == author.value:
                found_soundtracks.append(soundtrack)
                
        return found_soundtracks

    def update(self, soundtrack_to_update: Soundtrack):
        for soundtrack in self.__soundtracks:
            if soundtrack.soundtrack_id.value == soundtrack_to_update.soundtrack_id.value:
                self.__soundtracks.remove(soundtrack)
        self.__soundtracks.append(soundtrack_to_update)

    def delete(self, soundtrack_id: SoundtrackId):
        self.__soundtracks = [soundtrack for soundtrack in self.__soundtracks if soundtrack.soundtrack_id != soundtrack_id]
                    