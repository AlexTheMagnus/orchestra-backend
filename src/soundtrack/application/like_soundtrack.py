from ..domain.exceptions.already_liked_soundtrack_error import AlreadyLikedSoundtrackError
from ..domain.soundtrack_id import SoundtrackId
from ..domain.soundtrack_repository import SoundtrackRepository
from ..domain.user_id import UserId


class LikeSoundtrack():
    def __init__(self, soundtrack_repository: SoundtrackRepository):
        self.__soundtrack_repository = soundtrack_repository

    def run(self, user_id: UserId, soundtrack_id: SoundtrackId):

        if user_id in self.__soundtrack_repository.get_likes(soundtrack_id):
            raise(AlreadyLikedSoundtrackError(user_id.value, soundtrack_id.value))

        self.__soundtrack_repository.save_like(user_id, soundtrack_id)
