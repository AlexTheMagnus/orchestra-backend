from ..domain.soundtrack_id import SoundtrackId
from ..domain.soundtrack_repository import SoundtrackRepository
from ..domain.user_id import UserId
from ..domain.exceptions.unexisting_like_error import UnexistingLikeError


class UnlikeSoundtrack():
    def __init__(self, soundtrack_repository: SoundtrackRepository):
        self.__soundtrack_repository = soundtrack_repository

    def run(self, user_id: UserId, soundtrack_id: SoundtrackId):
        likes = self.__soundtrack_repository.get_likes(soundtrack_id)
        str_likes = [like.value for like in likes]

        if not any(str_like == user_id.value for str_like in str_likes):
            raise(UnexistingLikeError(user_id.value, soundtrack_id.value))

        self.__soundtrack_repository.delete_like(user_id, soundtrack_id)
