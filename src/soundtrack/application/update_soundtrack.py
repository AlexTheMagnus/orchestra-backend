from typing import TypedDict, Union

from ..domain.soundtrack_repository import SoundtrackRepository
from ..domain.soundtrack import Soundtrack
from ..domain.soundtrack_id import SoundtrackId
from ..domain.soundtrack_title import SoundtrackTitle
from ..domain.isbn_13 import Isbn13
from ..domain.exceptions.unexisting_soundtrack_error import UnexistingSoundtrackError

class NewSoundtrackData(TypedDict):
    book: Union[str, None]
    soundtrack_title: Union[str, None]

class UpdateSoundtrack():
    def __init__(self, soundtrack_repository: SoundtrackRepository):
        self.__soundtrack_repository = soundtrack_repository

    def run(self, soundtrack_id: SoundtrackId, new_data: NewSoundtrackData):
        found_soundtrack = self.__soundtrack_repository.find(soundtrack_id)
        if not found_soundtrack:
            raise(UnexistingSoundtrackError(soundtrack_id.value))

        if (new_data['book']):
            book = new_data['book']
        else:
            book = found_soundtrack.book

        if (new_data['soundtrack_title']):
            soundtrack_title = new_data['soundtrack_title']
        else:
            soundtrack_title = found_soundtrack.soundtrack_title

        updated_soundtrack: Soundtrack = Soundtrack(found_soundtrack.soundtrack_id, 
            book, soundtrack_title, found_soundtrack.author, [])

        self.__soundtrack_repository.update(updated_soundtrack)