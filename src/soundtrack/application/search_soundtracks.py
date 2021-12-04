from ..domain.isbn_13 import Isbn13
from ..domain.soundtrack_repository import SoundtrackRepository
from ..domain.search_options import SearchOptions

class SearchSoundtracks():
    def __init__(self, soundtrack_repository: SoundtrackRepository):
        self.__soundtrack_repository = soundtrack_repository

    def run(self, search_options: SearchOptions):
        return self.__soundtrack_repository.search(search_options)[:20]
