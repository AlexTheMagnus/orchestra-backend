from ..domain.exceptions.unexisting_favorite_error import UnexistingFavoriteError
from ..domain.soundtrack_id import SoundtrackId
from ..domain.user_id import UserId
from ..domain.user_repository import UserRepository

class RemoveSoundtrackFromFavorites():
    def __init__(self, user_repository: UserRepository):
        self.__user_repository = user_repository

    def run(self, user_id: UserId, soundtrack_id: SoundtrackId):
        favorite_soundtracks = self.__user_repository.get_favorites(user_id)
        str_favorite_soundtracks = [soundtrack.value for soundtrack in favorite_soundtracks]

        if not any(str_soundtrack_id == soundtrack_id.value for str_soundtrack_id in str_favorite_soundtracks):
            raise(UnexistingFavoriteError(user_id.value, soundtrack_id.value))

        self.__user_repository.remove_favorite(user_id, soundtrack_id)
