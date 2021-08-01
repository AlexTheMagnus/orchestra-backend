from ..domain.user_repository import UserRepository
from ..domain.user_id import UserId

class GetUserInfo():
    def __init__(self, user_repository: UserRepository):
        self.__user_repository = user_repository

    def run(self, user_id: UserId):
        return self.__user_repository.find(user_id)