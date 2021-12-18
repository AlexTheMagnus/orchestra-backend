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


class Follow:
    def __init__(self, follower_id: UserId, followed_id: UserId):
        self.__follower_id: UserId = follower_id
        self.__followed_id: UserId = followed_id

    @property
    def follower_id(self):
        return self.__follower_id

    @property
    def followed_id(self):
        return self.__followed_id


class UserInMemoryRepository(UserRepository):
    def __init__(self):
        self.__users: List[User] = []
        self.__favorites: List[Favorite] = []
        self.__follows: List[Follow] = []


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


    def remove_favorite(self, user_id: UserId, soundtrack_id: SoundtrackId):
        self.__favorites = [favorite for favorite in self.__favorites if ((favorite.soundtrack_id.value != soundtrack_id.value) or (favorite.user_id.value != user_id.value))]


    def save_follow(self, follower_id: UserId, followed_id: UserId):
        follow = Follow(follower_id, followed_id)
        self.__follows.append(follow)


    def get_followers(self, user_id: UserId) -> List[User]:
        found_follower_ids: List[UserId] = []
        found_followers: List[User] = []

        for follow in self.__follows:
            if follow.followed_id.value == user_id.value:
                found_follower_ids.append(follow.follower_id)
                
        for follower_id in found_follower_ids:
            for user in self.__users:
                if user.user_id.value == follower_id.value:
                    found_followers.append(user)

        return found_followers


    def get_followed_users(self, user_id: UserId) -> List[User]:
        found_followed_user_ids: List[UserId] = []
        found_followed_users: List[User] = []

        for follow in self.__follows:
            if follow.follower_id.value == user_id.value:
                found_followed_user_ids.append(follow.followed_id)
                
        for followed_user_id in found_followed_user_ids:
            for user in self.__users:
                if user.user_id.value == followed_user_id.value:
                    found_followed_users.append(user)

        return found_followed_users


    def unfollow_user(self, follower_id: UserId, followed_id: UserId):
        self.__follows = [follow for follow in self.__follows if ((follow.follower_id.value != follower_id.value) or (follow.followed_id.value != followed_id.value))]
