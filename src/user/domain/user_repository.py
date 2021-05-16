from abc import ABC, abstractmethod
from src.user.domain.user import User
from src.user.domain.user_id import UserId


class UserRepository(ABC):
    @abstractmethod
    def save(self, user: User):
        pass

    def find(self, user_id: UserId) -> User:
        pass
