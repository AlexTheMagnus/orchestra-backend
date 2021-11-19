from typing import List, Optional

from src.user.domain.soundtrack_id import SoundtrackId
from src.user.domain.user import User
from src.user.domain.user_id import UserId
from src.user.domain.user_repository import UserRepository

class Favorite:
    def __init__(self, user_id: UserId, soundtrack_id: SoundtrackId):
        self.__user_id: UserId = user_id
        self.__soundtrack_id: SoundtrackId = soundtrack_id

    @property
    def user_id(self):
        return self.__user_id

    @property
    def soundtrack_id(self):
        return self.__soundtrack_id


class UserInMemoryRepository(UserRepository):
    def __init__(self):
        self.__users: List[User] = []
        self.__favorites: List[Favorite] = []


    def save(self, user: User):
        self.__users.append(user)


    def find(self, user_id: UserId) -> Optional[User]:

        for user in self.__users:
            if user.user_id.value == user_id.value:
                return user
        return None


    def save_favorite(self, user_id: UserId, soundtrack_id: SoundtrackId):
        favorite = Favorite(user_id, soundtrack_id)
        self.__favorites.append(favorite)


    def get_favorites(self, user_id: UserId) -> List[SoundtrackId]:
        found_favorites: List[UserId] = []

        for favorite in self.__favorites:
            if favorite.user_id.value == user_id.value:
                found_favorites.append(favorite.soundtrack_id)
                
        return found_favorites