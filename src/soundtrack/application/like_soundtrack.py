from ..domain.exceptions.already_liked_soundtrack_error import AlreadyLikedSoundtrackError
from ..domain.exceptions.unexisting_soundtrack_error import UnexistingSoundtrackError
from ..domain.soundtrack_id import SoundtrackId
from ..domain.soundtrack_repository import SoundtrackRepository
from ..domain.user_id import UserId


class LikeSoundtrack():
    def __init__(self, soundtrack_repository: SoundtrackRepository):
        self.__soundtrack_repository = soundtrack_repository

    def run(self, user_id: UserId, soundtrack_id: SoundtrackId):
        if not self.__soundtrack_repository.find(soundtrack_id):
            raise(UnexistingSoundtrackError(soundtrack_id.value))

        for like in self.__soundtrack_repository.get_likes(soundtrack_id):
            if user_id.value == like.value:
                raise(AlreadyLikedSoundtrackError(user_id.value, soundtrack_id.value))

        self.__soundtrack_repository.save_like(user_id, soundtrack_id)
