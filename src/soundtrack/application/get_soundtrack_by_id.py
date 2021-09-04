from ..domain.soundtrack_repository import SoundtrackRepository
from ..domain.soundtrack_id import SoundtrackId
from ..domain.exceptions.unexisting_soundtrack_error import UnexistingSoundtrackError

class GetSoundtrackById():
    def __init__(self, soundtrack_repository: SoundtrackRepository):
        self.__soundtrack_repository = soundtrack_repository

    def run(self, soundtrack_id: SoundtrackId):

        found_soundtrack = self.__soundtrack_repository.find(soundtrack_id)
        if found_soundtrack == None:
            raise(UnexistingSoundtrackError(soundtrack_id))

        return found_soundtrack
