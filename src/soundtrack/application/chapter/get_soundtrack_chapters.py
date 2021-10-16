from ...domain.chapter.chapter_repository import ChapterRepository
from ...domain.soundtrack_id import SoundtrackId

class GetSoundtrackChapters():
    def __init__(self, chapter_repository: ChapterRepository):
        self.__chapter_repository = chapter_repository

    def run(self, soundtrack_id: SoundtrackId):
        return self.__chapter_repository.find_by_soundtrack(soundtrack_id)
