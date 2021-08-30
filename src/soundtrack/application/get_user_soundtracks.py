from ..domain.soundtrack_repository import SoundtrackRepository
from ..domain.user_id import UserId

class GetUserSoundtracks():
    def __init__(self, soundtrack_repository: SoundtrackRepository):
        self.__soundtrack_repository = soundtrack_repository

    def run(self, author: UserId):
        return self.__soundtrack_repository.find_by_author(author)
