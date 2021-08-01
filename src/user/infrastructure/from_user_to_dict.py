from ..domain.user import User


class FromUserToDict:

    def __init__(self):
        pass

    @staticmethod
    def with_user(user: User):
        user_dict = {
            "user_id": user.user_id.value,
            "username": user.username.value,
            "user_avatar": user.user_avatar.value
        }

        return user_dict