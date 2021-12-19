from typing import List

from ..domain.chapter.chapter import Chapter
from ..domain.chapter.chapter_repository import ChapterRepository
from ..domain.exceptions.unexisting_soundtrack_error import UnexistingSoundtrackError
from ..domain.favorite_repository import FavoriteRepository
from ..domain.soundtrack_id import SoundtrackId
from ..domain.soundtrack_repository import SoundtrackRepository
from ..domain.user_id import UserId

class DeleteSoundtrack():
    def __init__(self, soundtrack_repository: SoundtrackRepository, chapter_repository: ChapterRepository, favorite_repository: FavoriteRepository):
        self.__soundtrack_repository = soundtrack_repository
        self.__chapter_repository = chapter_repository
        self.__favorite_repository = favorite_repository

    def run(self, soundtrack_id: SoundtrackId):
        self.__favorite_repository.delete_all_with_soundtrack(soundtrack_id)

        soundtrack_likes: List[UserId] = self.__soundtrack_repository.get_likes(soundtrack_id)
        for user_id in soundtrack_likes:
            self.__soundtrack_repository.delete_like(user_id, soundtrack_id)

        soundtrack_chapters: List[Chapter] = self.__chapter_repository.find_by_soundtrack(soundtrack_id)
        for chapter in soundtrack_chapters:
            self.__chapter_repository.delete(chapter.chapter_id)

        soundtrack_to_be_deleted = self.__soundtrack_repository.find(soundtrack_id)
        if soundtrack_to_be_deleted == None:
            raise(UnexistingSoundtrackError(soundtrack_id.value))

        self.__soundtrack_repository.delete(soundtrack_id)
