from flask import Blueprint, abort, jsonify, request
from typing import List
import os

from ..application.create_soundtrack import CreateSoundtrack
from ..application.delete_soundtrack import DeleteSoundtrack
from ..application.get_soundtrack_by_id import GetSoundtrackById
from ..application.get_soundtrack_likes import GetSoundtrackLikes
from ..application.get_user_soundtracks import GetUserSoundtracks
from ..application.like_soundtrack import LikeSoundtrack
from ..application.search_soundtracks import SearchSoundtracks
from ..application.unlike_soundtrack import UnlikeSoundtrack
from ..application.update_soundtrack import UpdateSoundtrack
from ..domain.chapter.chapter import Chapter
from ..domain.exceptions.already_existing_soundtrack_error import AlreadyExistingSoundtrackError
from ..domain.exceptions.already_liked_soundtrack_error import AlreadyLikedSoundtrackError
from ..domain.exceptions.unexisting_like_error import UnexistingLikeError
from ..domain.exceptions.unexisting_soundtrack_error import UnexistingSoundtrackError
from ..domain.exceptions.unexisting_soundtrack_error import UnexistingSoundtrackError
from ..domain.isbn_13 import Isbn13
from ..domain.search_options import SearchOptions
from ..domain.soundtrack import Soundtrack
from ..domain.soundtrack_id import SoundtrackId
from ..domain.soundtrack_title import SoundtrackTitle
from ..domain.user_id import UserId
from .chapter.chapter_mysql_repository import ChapterMysqlRepository
from .favorite_mysql_repository import FavoriteMysqlRepository
from .from_soundtrack_to_dict import FromSoundtrackToDict
from .soundtrack_mysql_repository import SoundtrackMysqlRepository
from .validators.access_token_validator import AccessTokenValidator
from .validators.soundtracks_like_post_validator import SoundtracksLikePostValidator
from .validators.soundtracks_post_validator import SoundtracksPostValidator
from .validators.soundtracks_put_validator import SoundtracksPutValidator
from .validators.soundtracks_search_post_validator import SoundtracksSearchPostValidator

soundtracks = Blueprint("soundtracks", __name__, url_prefix="/soundtracks")


@soundtracks.route('', methods=["POST"])
def create_soundtrack():
    if not SoundtracksPostValidator().validate(request.json):
        abort(400)

    if not "PYTEST_CURRENT_TEST" in os.environ:
        access_token = request.headers['Authorization'].replace("Bearer ", "") if 'Authorization' in request.headers else ''
        logged_user = AccessTokenValidator.validate(access_token)
        if not logged_user:
            abort(401)

        if logged_user['id'] != request.json['author']:
            abort(403)

    soundtrack_repository = SoundtrackMysqlRepository()

    soundtrack = Soundtrack(
        soundtrack_id=SoundtrackId.from_string(request.json['soundtrack_id']),
        book=Isbn13.from_string(request.json['book']),
        soundtrack_title=SoundtrackTitle.from_string(
            request.json['soundtrack_title']),
        author=UserId.from_string(request.json['author']),
    )

    try:
        CreateSoundtrack(soundtrack_repository).run(soundtrack)
    except Exception as error:
        if isinstance(error, AlreadyExistingSoundtrackError):
            abort(409)
        else:
            abort(500)

    return '200'


@soundtracks.route('/user/<string:str_author>', methods=["GET"])
def get_user_soundtracks(str_author: str):
    soundtrack_repository = SoundtrackMysqlRepository()
    author = UserId.from_string(str_author)

    try:
        soundtracks_list = GetUserSoundtracks(soundtrack_repository).run(author)
    except Exception as error:
        abort(500)

    return jsonify(FromSoundtrackToDict.with_soundtracks_list(soundtracks_list)), '200'


@soundtracks.route('/<string:str_soundtrack_id>', methods=["GET"])
def get_soundtrack_by_id(str_soundtrack_id: str):
    soundtrack_repository = SoundtrackMysqlRepository()
    soundtrack_id: SoundtrackId = SoundtrackId.from_string(str_soundtrack_id)

    try:
        soundtrack = GetSoundtrackById(soundtrack_repository).run(soundtrack_id)
    except Exception as error:
        if isinstance(error, UnexistingSoundtrackError):
            abort(404)
        else:
            abort(500)

    return jsonify(FromSoundtrackToDict.with_soundtrack(soundtrack)), '200'


@soundtracks.route('/search', methods=["POST"])
def search_soundtracks():
    if not SoundtracksSearchPostValidator().validate(request.json):
        abort(400)

    soundtrack_repository = SoundtrackMysqlRepository()
    search_options: SearchOptions = {"book": Isbn13.from_string(request.json['book'])}

    try:
        search_results = SearchSoundtracks(soundtrack_repository).run(search_options)
    except Exception as error:
        abort(500)

    return jsonify(FromSoundtrackToDict.with_soundtracks_list(search_results)), '200'


@soundtracks.route('/update/<string:str_soundtrack_id>', methods=["PUT"])
def update_soundtrack(str_soundtrack_id: str):
    if not SoundtracksPutValidator().validate(request.json):
        abort(400)

    soundtrack_repository = SoundtrackMysqlRepository()
    soundtrack_id = SoundtrackId.from_string(str_soundtrack_id)

    if not "PYTEST_CURRENT_TEST" in os.environ:
        access_token = request.headers['Authorization'].replace("Bearer ", "") if 'Authorization' in request.headers else ''
        logged_user = AccessTokenValidator.validate(access_token)
        if not logged_user:
            abort(401)

        soundtrack_to_be_updated = soundtrack_repository.find(soundtrack_id)
        if soundtrack_to_be_updated != None and logged_user['id'] != soundtrack_to_be_updated.author.value:
            abort(403)

    if ('book' in request.json):
        book = Isbn13.from_string(request.json['book'])
    else:
        book = None

    if ('soundtrack_title' in request.json):
        soundtrack_title = SoundtrackTitle.from_string(request.json['soundtrack_title'])
    else:
        soundtrack_title = None

    try:
        UpdateSoundtrack(soundtrack_repository).run(soundtrack_id,
         {'soundtrack_title': soundtrack_title,  'book': book})
    except Exception as error:
        if isinstance(error, UnexistingSoundtrackError):
            abort(404)
        else:
            abort(500)

    return '200'


@soundtracks.route('/delete/<string:str_soundtrack_id>', methods=["DELETE"])
def delete_soundtrack(str_soundtrack_id: str):
    soundtrack_repository = SoundtrackMysqlRepository()
    soundtrack_id = SoundtrackId.from_string(str_soundtrack_id)
    
    if not "PYTEST_CURRENT_TEST" in os.environ:
        access_token = request.headers['Authorization'].replace("Bearer ", "") if 'Authorization' in request.headers else ''
        logged_user = AccessTokenValidator.validate(access_token)
        if not logged_user:
            abort(401)

        soundtrack_to_be_deleted = soundtrack_repository.find(soundtrack_id)
        if soundtrack_to_be_deleted != None and logged_user['id'] != soundtrack_to_be_deleted.author.value:
            abort(403)

    chapter_repository = ChapterMysqlRepository()
    favorite_repository = FavoriteMysqlRepository()
    
    try:
        DeleteSoundtrack(soundtrack_repository, chapter_repository, favorite_repository).run(soundtrack_id)
    except Exception as error:
        if isinstance(error, UnexistingSoundtrackError):
            abort(404)
        else:
            abort(500)

    return ('', 204)


@soundtracks.route('/like', methods=["POST"])
def like_soundtrack():
    if not SoundtracksLikePostValidator().validate(request.json):
        abort(400)

    if not "PYTEST_CURRENT_TEST" in os.environ:
        access_token = request.headers['Authorization'].replace("Bearer ", "") if 'Authorization' in request.headers else ''
        logged_user = AccessTokenValidator.validate(access_token)
        if not logged_user:
            abort(401)

        if logged_user['id'] != request.json['user_id']:
            abort(403)

    soundtrack_repository = SoundtrackMysqlRepository()
    
    user_id = UserId.from_string(request.json['user_id'])
    soundtrack_id = SoundtrackId.from_string(request.json['soundtrack_id'])

    try:
        LikeSoundtrack(soundtrack_repository).run(user_id, soundtrack_id)
    except Exception as error:
        if isinstance(error, UnexistingSoundtrackError):
            abort(404)
        if isinstance(error, AlreadyLikedSoundtrackError):
            abort(409)
        else:
            abort(500)

    return '200'


@soundtracks.route('/<string:str_soundtrack_id>/likes', methods=["GET"])
def get_soundtrack_likes(str_soundtrack_id: str):
    soundtrack_repository = SoundtrackMysqlRepository()
    soundtrack_id = SoundtrackId.from_string(str_soundtrack_id)

    try:
        likes_list = GetSoundtrackLikes(soundtrack_repository).run(soundtrack_id)
    except Exception as error:
        abort(500)

    likes_list_dict = { "likes_list": [like.value for like in likes_list] }

    return jsonify(likes_list_dict), '200'


@soundtracks.route('/<string:str_soundtrack_id>/unlike/<string:str_user_id>', methods=["DELETE"])
def unlike_soundtrack(str_soundtrack_id: str, str_user_id: str):
    if not "PYTEST_CURRENT_TEST" in os.environ:
        access_token = request.headers['Authorization'].replace("Bearer ", "") if 'Authorization' in request.headers else ''
        logged_user = AccessTokenValidator.validate(access_token)
        if not logged_user:
            abort(401)

        if logged_user['id'] != str_user_id:
            abort(403)

    soundtrack_repository = SoundtrackMysqlRepository()
    user_id = UserId.from_string(str_user_id)
    soundtrack_id = SoundtrackId.from_string(str_soundtrack_id)
    
    try:
        UnlikeSoundtrack(soundtrack_repository).run(user_id, soundtrack_id)
    except Exception as error:
        if isinstance(error, UnexistingLikeError):
            abort(404)
        else:
            abort(500)

    return ('', 204)


