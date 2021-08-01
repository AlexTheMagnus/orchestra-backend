from flask import Blueprint, abort, request

from .user_mysql_repository import UserMysqlRepository
from ..domain.user_id import UserId
from ..domain.username import Username
from ..domain.user_avatar import UserAvatar
from ..domain.user import User
from ..application.register_user import RegisterUser
from .validators.users_post_validator import UsersPostValidator

users = Blueprint("users", __name__, url_prefix="/users")


@users.route('', methods=["POST"])
def register_user():
    user_repository = UserMysqlRepository()

    if not UsersPostValidator().validate(request.json):
        abort(400)

    user = User(
        user_id=UserId.from_string(request.json['user_id']),
        username=Username.from_string(request.json['username']),
        user_avatar=UserAvatar.from_url(request.json['user_avatar'])
    )

    try:
        RegisterUser(user_repository).run(user)
    except Exception as error:
        if isinstance(error, AlreadyExistingUserError):
            abort(409)
        else:
            abort(500)

    return '200'
