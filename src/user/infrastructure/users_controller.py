from flask import Blueprint, abort, jsonify, request
from spotipy import oauth2, client
import os
import spotipy

from ..application.add_soundtrack_to_favorites import AddSoundtrackToFavorites
from ..application.follow_user import FollowUser
from ..application.get_followed_users import GetFollowedUsers
from ..application.get_followers import GetFollowers
from ..application.get_user_favorites import GetUserFavorites
from ..application.get_user_info import GetUserInfo
from ..application.register_user import RegisterUser
from ..application.remove_soundtrack_from_favorites import RemoveSoundtrackFromFavorites
from ..application.unfollow_user import UnfollowUser
from ..domain.exceptions.already_existing_user_error import AlreadyExistingUserError
from ..domain.exceptions.soundtrack_already_added_to_favorites_error import SoundtrackAlreadyAddedToFavoritesError
from ..domain.exceptions.unexisting_favorite_error import UnexistingFavoriteError
from ..domain.exceptions.unexisting_follow_error import UnexistingFollowError
from ..domain.exceptions.unexisting_soundtrack_error import UnexistingSoundtrackError
from ..domain.exceptions.unexisting_user_error import UnexistingUserError
from ..domain.exceptions.user_already_followed_error import UserAlreadyFollowedError
from ..domain.soundtrack_id import SoundtrackId
from ..domain.user import User
from ..domain.user_avatar import UserAvatar
from ..domain.user_id import UserId
from ..domain.username import Username
from .from_user_to_dict import FromUserToDict
from .soundtrack_mysql_reporter import SoundtrackMysqlReporter
from .user_mysql_repository import UserMysqlRepository
from .validators.access_token_validator import AccessTokenValidator
from .validators.users_favorite_post_validator import UsersFavoritePostValidator
from .validators.users_follow_post_validator import UsersFollowPostValidator
from .validators.users_post_validator import UsersPostValidator

users = Blueprint("users", __name__, url_prefix="/users")

@users.route('', methods=["POST"])
def user_access():
    if not UsersPostValidator().validate(request.json):
        abort(400)

    user_repository = UserMysqlRepository()
    spotify_oauth = oauth2.SpotifyOAuth(
        client_id=os.getenv('CLIENT_ID'), client_secret=os.getenv('CLIENT_SECRET'),
        redirect_uri=os.getenv('SPOTIPY_REDIRECT_URI')
    )

    token_info = spotify_oauth.get_access_token(code=request.json['access_code'])
    access_token = token_info['access_token']
    spotipy_client = client.Spotify(auth=access_token)
    spotify_user = spotipy_client.me()

    user_id = UserId.from_string(spotify_user['id'])
    username = Username.from_string(spotify_user['display_name'])
    user_avatar = UserAvatar.from_url(spotify_user['images'][0]['url'] if len(spotify_user['images']) >= 1 else "")
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

    cleanCache()

    return jsonify(dictResponse), '200'

def cleanCache():
    os.remove('.cache')

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
    if not UsersFavoritePostValidator().validate(request.json):
        abort(400)

    if not "PYTEST_CURRENT_TEST" in os.environ:
        access_token = request.headers['Authorization'].replace("Bearer ", "") if 'Authorization' in request.headers else ''
        logged_user = AccessTokenValidator.validate(access_token)
        if not logged_user:
            abort(401)

        if logged_user['id'] != request.json['user_id']:
            abort(403)

    user_repository = UserMysqlRepository()
    soundtrack_reporter = SoundtrackMysqlReporter()
    
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
    if not "PYTEST_CURRENT_TEST" in os.environ:
        access_token = request.headers['Authorization'].replace("Bearer ", "") if 'Authorization' in request.headers else ''
        logged_user = AccessTokenValidator.validate(access_token)
        if not logged_user:
            abort(401)

        if logged_user['id'] != str_user_id:
            abort(403)
            
    user_repository = UserMysqlRepository()
    user_id = UserId.from_string(str_user_id)
    soundtrack_id = SoundtrackId.from_string(str_soundtrack_id)
    
    try:
        RemoveSoundtrackFromFavorites(user_repository).run(user_id, soundtrack_id)
    except Exception as error:
        if isinstance(error, UnexistingFavoriteError):
            abort(404)
        else:
            abort(500)

    return ('', 204)


@users.route('/follow', methods=["POST"])
def follow_user():
    if not "PYTEST_CURRENT_TEST" in os.environ:
        access_token = request.headers['Authorization'].replace("Bearer ", "") if 'Authorization' in request.headers else ''
        logged_user = AccessTokenValidator.validate(access_token)
        if not logged_user:
            abort(401)

        if logged_user['id'] != request.json['follower_id']:
            abort(403)

    user_repository = UserMysqlRepository()

    if not UsersFollowPostValidator().validate(request.json):
        abort(400)
    
    follower_id = UserId.from_string(request.json['follower_id'])
    followed_id = UserId.from_string(request.json['followed_id'])

    try:
        FollowUser(user_repository).run(follower_id, followed_id)
    except Exception as error:
        if isinstance(error, UnexistingUserError):
            abort(404)
        if isinstance(error, UserAlreadyFollowedError):
            abort(409)
        else:
            abort(500)

    return '200'


@users.route('/<string:str_user_id>/followers', methods=["GET"])
def get_followers(str_user_id: str):
    user_repository = UserMysqlRepository()

    user_id = UserId.from_string(str_user_id)

    try:
        follower_list = GetFollowers(user_repository).run(user_id)
    except Exception as error:
        abort(500)

    follower_list_dict = { 
        "followers": FromUserToDict.with_user_list(follower_list)
    }

    return jsonify(follower_list_dict), '200'


@users.route('/<string:str_user_id>/followed-users', methods=["GET"])
def get_followed_users(str_user_id: str):
    user_repository = UserMysqlRepository()

    user_id = UserId.from_string(str_user_id)

    try:
        followed_user_list = GetFollowedUsers(user_repository).run(user_id)
    except Exception as error:
        abort(500)

    followed_user_list_dict = { 
        "followed_users": FromUserToDict.with_user_list(followed_user_list)
    }

    return jsonify(followed_user_list_dict), '200'


@users.route('/<string:str_follower_id>/unfollow/<string:str_followed_user_id>', methods=["DELETE"])
def unfollow_user(str_follower_id: str, str_followed_user_id: str):
    if not "PYTEST_CURRENT_TEST" in os.environ:
        access_token = request.headers['Authorization'].replace("Bearer ", "") if 'Authorization' in request.headers else ''
        logged_user = AccessTokenValidator.validate(access_token)
        if not logged_user:
            abort(401)

        if logged_user['id'] != str_follower_id:
            abort(403)

    user_repository = UserMysqlRepository()
    follower_id = UserId.from_string(str_follower_id)
    followed_user_id = UserId.from_string(str_followed_user_id)
    
    try:
        UnfollowUser(user_repository).run(follower_id, followed_user_id)
    except Exception as error:
        if isinstance(error, UnexistingFollowError):
            abort(404)
        else:
            abort(500)

    return ('', 204)
