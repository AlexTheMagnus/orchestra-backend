from flask import Blueprint, abort, jsonify, request
from spotipy import oauth2, client
import os
import spotipy

from ..application.add_soundtrack_to_favorites import AddSoundtrackToFavorites
from ..application.get_user_favorites import GetUserFavorites
from ..application.get_user_info import GetUserInfo
from ..application.register_user import RegisterUser
from ..application.remove_soundtrack_from_favorites import RemoveSoundtrackFromFavorites
from ..domain.exceptions.already_existing_user_error import AlreadyExistingUserError
from ..domain.exceptions.soundtrack_already_added_to_favorites_error import SoundtrackAlreadyAddedToFavoritesError
from ..domain.exceptions.unexisting_favorite_error import UnexistingFavoriteError
from ..domain.exceptions.unexisting_soundtrack_error import UnexistingSoundtrackError
from ..domain.exceptions.unexisting_user_error import UnexistingUserError
from ..domain.soundtrack_id import SoundtrackId
from ..domain.user import User
from ..domain.user_avatar import UserAvatar
from ..domain.user_id import UserId
from ..domain.username import Username
from .from_user_to_dict import FromUserToDict
from .soundtrack_mysql_reporter import SoundtrackMysqlReporter
from .user_mysql_repository import UserMysqlRepository
from .validators.users_favorite_post_validator import UsersFavoritePostValidator
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
        abort(500)

    return jsonify(FromUserToDict.with_user(user)), '200'


@users.route('/favorite', methods=["POST"])
def add_soundtrack_to_favorites():
    user_repository = UserMysqlRepository()
    soundtrack_reporter = SoundtrackMysqlReporter()

    if not UsersFavoritePostValidator().validate(request.json):
        abort(400)
    
    user_id = UserId.from_string(request.json['user_id'])
    soundtrack_id = SoundtrackId.from_string(request.json['soundtrack_id'])

    try:
        AddSoundtrackToFavorites(user_repository, soundtrack_reporter).run(user_id, soundtrack_id)
    except Exception as error:
        if isinstance(error, UnexistingSoundtrackError):
            abort(404)
        if isinstance(error, UnexistingUserError):
            abort(404)
        if isinstance(error, SoundtrackAlreadyAddedToFavoritesError):
            abort(409)
        else:
            abort(500)

    return '200'


@users.route('/<string:str_user_id>/favorites', methods=["GET"])
def get_user_favorites(str_user_id: str):
    user_repository = UserMysqlRepository()
    user_id = UserId.from_string(str_user_id)

    try:
        favorites_list = GetUserFavorites(user_repository).run(user_id)
    except Exception as error:
        abort(500)

    favorites_list_dict = { 
        "favorite_soundtracks_list": [favorite_soundtrack.value for favorite_soundtrack in favorites_list]
    }

    return jsonify(favorites_list_dict), '200'


@users.route('/<string:str_user_id>/unfavorite/<string:str_soundtrack_id>', methods=["DELETE"])
def remove_soundtrack_from_favorites(str_user_id: str, str_soundtrack_id: str):
    user_repository = UserMysqlRepository()
    user_id = UserId.from_string(str_user_id)
    soundtrack_id = SoundtrackId.from_string(str_soundtrack_id)
    
    try:
        RemoveSoundtrackFromFavorites(user_repository).run(user_id, soundtrack_id)
    except Exception as error:
        if isinstance(error, UnexistingFavoriteError):
            abort(404)
        else:
            print(error)
            abort(500)

    return ('', 204)