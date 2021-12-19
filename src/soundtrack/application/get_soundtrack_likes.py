from typing import List

from ..domain.soundtrack_repository import SoundtrackRepository
from ..domain.soundtrack_id import SoundtrackId
from ..domain.user_id import UserId

class GetSoundtrackLikes():
    def __init__(self, soundtrack_repository: SoundtrackRepository):
        self.__soundtrack_repository = soundtrack_repository

    def run(self, soundtrack_id: SoundtrackId) -> List[UserId]:
        return self.__soundtrack_repository.get_likes(soundtrack_id)
