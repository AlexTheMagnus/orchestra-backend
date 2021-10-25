from ..domain.soundtrack_repository import SoundtrackRepository
from ..domain.soundtrack import Soundtrack
from ..domain.exceptions.unexisting_soundtrack_error import UnexistingSoundtrackError

class EditSoundtrack():
    def __init__(self, soundtrack_repository: SoundtrackRepository):
        self.__soundtrack_repository = soundtrack_repository

    def run(self, soundtrack: Soundtrack):

        if not self.__soundtrack_repository.find(soundtrack.soundtrack_id):
            raise(UnexistingSoundtrackError(soundtrack.soundtrack_id.value))

        self.__soundtrack_repository.update(soundtrack)