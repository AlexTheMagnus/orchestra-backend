from flask import Blueprint, abort, jsonify, request

from .user_mysql_repository import UserMysqlRepository
from ..domain.user_id import UserId
from ..domain.username import Username
from ..domain.user_avatar import UserAvatar
from ..domain.user import User
from ..application.register_user import RegisterUser
from ..application.get_user_info import GetUserInfo
from ..domain.exceptions.already_existing_user_error import AlreadyExistingUserError
from .from_user_to_dict import FromUserToDict
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


@users.route('/<string:str_user_id>', methods=["GET"])
def get_user_info(str_user_id: str):
    user_repository = UserMysqlRepository()

    user_id = UserId.from_string(str_user_id)

    try:
        user = GetUserInfo(user_repository).run(user_id)
    except Exception as error:
        print(error)
        abort(500)

    return jsonify(FromUserToDict.with_user(user)), '200'
