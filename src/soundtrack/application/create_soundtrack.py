from src.soundtrack.domain.soundtrack_repository import SoundtrackRepository
from src.soundtrack.domain.soundtrack import Soundtrack
from src.soundtrack.domain.soundtrack_id import SoundtrackId
from src.soundtrack.domain.isbn_13 import Isbn13
from src.soundtrack.domain.user_id import UserId
from src.soundtrack.domain.chapter.chapter import Chapter
from src.soundtrack.domain.exceptions.already_existing_soundtrack_error import AlreadyExistingSoundtrackError


class CreateSoundtrack():
    def __init__(self, soundtrack_repository: SoundtrackRepository):
        self.__soundtrack_repository = soundtrack_repository

    def run(self, soundtrack: Soundtrack):

        if self.__soundtrack_repository.find(soundtrack.soundtrack_id):
            raise(AlreadyExistingSoundtrackError(soundtrack.soundtrack_id))

        self.__soundtrack_repository.save(soundtrack)
