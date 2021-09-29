from flask import Blueprint, abort, jsonify, request
import os
import spotipy
from spotipy import oauth2
from spotipy import client

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
def user_access():
    user_repository = UserMysqlRepository()
    spotify_oauth = oauth2.SpotifyOAuth( os.getenv('CLIENT_ID'), os.getenv('CLIENT_SECRET'), os.getenv('SPOTIPY_REDIRECT_URI'))

    if not UsersPostValidator().validate(request.json):
        abort(400)

    token_info = spotify_oauth.get_access_token(request.json['access_code'])
    access_token = token_info['access_token']
    spotipy_client = client.Spotify(auth=access_token)
    spotify_user = spotipy_client.me()

    user_id = UserId.from_string(spotify_user['id'])
    username = Username.from_string(spotify_user['display_name'])
    user_avatar = UserId.from_string(spotify_user['images'][0]['url'])
    user = User(user_id, username, user_avatar)

    if(user_repository.find(user_id) == None):
        try:
            RegisterUser(user_repository).run(user)
        except Exception as error:
            if isinstance(error, AlreadyExistingUserError):
                abort(409)
            else:
                abort(500)

    dictResponse = FromUserToDict.with_user(user)
    dictResponse['access_token'] = access_token
    
    return jsonify(dictResponse), '200'

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
