from ..domain.soundtrack_repository import SoundtrackRepository
from ..domain.soundtrack import SoundtrackId

class GetSoundtrackLikes():
    def __init__(self, soundtrack_repository: SoundtrackRepository):
        self.__soundtrack_repository = soundtrack_repository

    def run(self, soundtrack_id: SoundtrackId):
        return self.__soundtrack_repository.get_likes(soundtrack_id)
