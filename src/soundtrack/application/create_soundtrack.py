from ..domain.soundtrack_repository import SoundtrackRepository
from ..domain.soundtrack import Soundtrack
from ..domain.soundtrack_id import SoundtrackId
from ..domain.isbn_13 import Isbn13
from ..domain.user_id import UserId
from ..domain.chapter.chapter import Chapter
from ..domain.exceptions.already_existing_soundtrack_error import AlreadyExistingSoundtrackError


class CreateSoundtrack():
    def __init__(self, soundtrack_repository: SoundtrackRepository):
        self.__soundtrack_repository = soundtrack_repository

    def run(self, soundtrack: Soundtrack):

        if self.__soundtrack_repository.find(soundtrack.soundtrack_id):
            raise(AlreadyExistingSoundtrackError(soundtrack.soundtrack_id))

        self.__soundtrack_repository.save(soundtrack)
