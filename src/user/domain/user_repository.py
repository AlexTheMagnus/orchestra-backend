from abc import ABC, abstractmethod
from ..domain.user import User
from ..domain.user_id import UserId


class UserRepository(ABC):
    @abstractmethod
    def save(self, user: User):
        pass

    def find(self, user_id: UserId) -> User:
        pass
