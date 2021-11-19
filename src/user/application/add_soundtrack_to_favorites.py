from ..domain.exceptions.soundtrack_already_added_to_favorites_error import SoundtrackAlreadyAddedToFavoritesError
from ..domain.exceptions.unexisting_soundtrack_error import UnexistingSoundtrackError
from ..domain.exceptions.unexisting_user_error import UnexistingUserError
from ..domain.soundtrack_id import SoundtrackId
from ..domain.soundtrack_reporter import SoundtrackReporter
from ..domain.user_id import UserId
from ..domain.user_repository import UserRepository

class AddSoundtrackToFavorites():
    def __init__(self, user_repository: UserRepository, soundtrack_reporter: SoundtrackReporter):
        self.__user_repository = user_repository
        self.__soundtrack_reporter = soundtrack_reporter

    def run(self, user_id: UserId, soundtrack_id: SoundtrackId):
        if not self.__user_repository.find(user_id):
            raise(UnexistingUserError(user_id.value))

        if not self.__soundtrack_reporter.exist(soundtrack_id):
            raise(UnexistingSoundtrackError(soundtrack_id.value))

        print(self.__user_repository.get_favorites(user_id))
        for favorite_soundtrack_id in self.__user_repository.get_favorites(user_id):
            if soundtrack_id.value == favorite_soundtrack_id.value:
                raise(SoundtrackAlreadyAddedToFavoritesError(user_id.value, soundtrack_id.value))

        self.__user_repository.save_favorite(user_id, soundtrack_id)
