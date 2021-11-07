from typing import List, Optional

from src.soundtrack.domain.soundtrack_repository import SoundtrackRepository
from src.soundtrack.domain.soundtrack import Soundtrack
from src.soundtrack.domain.soundtrack_id import SoundtrackId
from src.soundtrack.domain.user_id import UserId

class Like:
    def __init__(self, user_id: UserId, soundtrack_id: SoundtrackId):
        self.__user_id: UserId = user_id
        self.__soundtrack_id: SoundtrackId = soundtrack_id

    @property
    def user_id(self):
        return self.__user_id

    @property
    def soundtrack_id(self):
        return self.__soundtrack_id


class SoundtrackInMemoryRepository(SoundtrackRepository):
    def __init__(self):
        self.__soundtracks: List[Soundtrack] = []
        self.__likes: List[Like] = []


    def save(self, soundtrack: Soundtrack):
        self.__soundtracks.append(soundtrack)


    def find(self, soundtrack_id: SoundtrackId) -> Optional[Soundtrack]:
        for soundtrack in self.__soundtracks:
            if soundtrack.soundtrack_id.value == soundtrack_id.value:
                return soundtrack

        return None


    def find_by_author(self, author: UserId) -> Optional[Soundtrack]:
        found_soundtracks: List[Soundtrack] = []

        for soundtrack in self.__soundtracks:
            if soundtrack.author.value == author.value:
                found_soundtracks.append(soundtrack)
                
        return found_soundtracks


    def update(self, soundtrack_to_update: Soundtrack):
        for soundtrack in self.__soundtracks:
            if soundtrack.soundtrack_id.value == soundtrack_to_update.soundtrack_id.value:
                self.__soundtracks.remove(soundtrack)
        self.__soundtracks.append(soundtrack_to_update)


    def delete(self, soundtrack_id: SoundtrackId):
        self.__soundtracks = [soundtrack for soundtrack in self.__soundtracks if soundtrack.soundtrack_id != soundtrack_id]


    def save_like(self, user_id: UserId, soundtrack_id: SoundtrackId):
        like = Like(user_id, soundtrack_id)
        self.__likes.append(like)

                    
    def get_likes(self, soundtrack_id: SoundtrackId):
        found_likes: List[UserId] = []

        for like in self.__likes:
            if like.soundtrack_id.value == soundtrack_id.value:
                found_likes.append(like.user_id)
                
        return found_likes


    def delete_like(self, user_id: UserId, soundtrack_id: SoundtrackId):
        print(self.__likes)
        self.__likes = [like for like in self.__likes if ((like.soundtrack_id.value != soundtrack_id.value) or (like.user_id.value != user_id.value))]
        print(self.__likes)
