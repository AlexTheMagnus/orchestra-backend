from src.user.domain.user_repository import UserRepository
from src.user.domain.user import User
from src.user.domain.already_existing_user_error import AlreadyExistingUserError


class RegisterUser():
    def __init__(self, user_repository: UserRepository):
        self.__user_repository = user_repository

    def run(self, user: User):

        if self.__user_repository.find(user.user_id):
            raise(AlreadyExistingUserError(user.user_id))

        self.__user_repository.save(user)
