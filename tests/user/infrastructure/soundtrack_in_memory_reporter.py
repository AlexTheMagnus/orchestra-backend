from src.user.domain.soundtrack_id import SoundtrackId
from src.user.domain.soundtrack_reporter import SoundtrackReporter
from ...soundtrack.infrastructure.soundtrack_in_memory_repository import SoundtrackInMemoryRepository

class SoundtrackInMemoryReporter(SoundtrackReporter):
    def __init__(self, soundtrack_repository: SoundtrackInMemoryRepository = []):
        self.__soundtrack_repository = soundtrack_repository

    def exist(self, soundtrack_id: SoundtrackId) -> bool:

        if self.__soundtrack_repository.find(soundtrack_id):
            return True
        return False
