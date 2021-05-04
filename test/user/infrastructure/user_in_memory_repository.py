from typing import List, Optional

from src.user.domain.user import User
from src.user.domain.user_id import UserId
from src.user.domain.user_repository import UserRepository


class UserInMemoryRepository(UserRepository):
    def __init__(self):
        self.__users: List[User] = []

    def save(self, user: User):
        self.__users.append(user)

    def find(self, user_id: UserId) -> Optional[User]:
        print("user_id:", user_id)

        for user in self.__users:
            if user.user_id.value == user_id.value:
                return user
        return None
