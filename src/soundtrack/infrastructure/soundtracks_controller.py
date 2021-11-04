from flask import Blueprint, abort, jsonify, request

from typing import List

from .soundtrack_mysql_repository import SoundtrackMysqlRepository
from .chapter.chapter_mysql_repository import ChapterMysqlRepository
from ..application.create_soundtrack import CreateSoundtrack
from ..application.get_user_soundtracks import GetUserSoundtracks
from ..application.get_soundtrack_by_id import GetSoundtrackById
from ..application.update_soundtrack import UpdateSoundtrack
from ..application.delete_soundtrack import DeleteSoundtrack
from ..domain.soundtrack import Soundtrack
from ..domain.soundtrack_id import SoundtrackId
from ..domain.isbn_13 import Isbn13
from ..domain.soundtrack_title import SoundtrackTitle
from ..domain.user_id import UserId
from ..domain.chapter.chapter import Chapter
from ..domain.exceptions.already_existing_soundtrack_error import AlreadyExistingSoundtrackError
from ..domain.exceptions.unexisting_soundtrack_error import UnexistingSoundtrackError
from ..domain.exceptions.already_liked_soundtrack_error import AlreadyLikedSoundtrackError
from .from_soundtrack_to_dict import FromSoundtrackToDict
from .validators.soundtracks_post_validator import SoundtracksPostValidator
from .validators.soundtracks_put_validator import SoundtracksPutValidator
from .validators.soundtracks_like_post_validator import SoundtracksLikePostValidator

soundtracks = Blueprint("soundtracks", __name__, url_prefix="/soundtracks")


@soundtracks.route('', methods=["POST"])
def create_soundtrack():
    soundtrack_repository = SoundtrackMysqlRepository()

    if not SoundtracksPostValidator().validate(request.json):
        abort(400)

    soundtrack = Soundtrack(
        soundtrack_id=SoundtrackId.from_string(request.json['soundtrack_id']),
        book=Isbn13.from_string(request.json['book']),
        soundtrack_title=SoundtrackTitle.from_string(
            request.json['soundtrack_title']),
        author=UserId.from_string(request.json['author']),
        chapters=[]
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


@soundtracks.route('/update/<string:str_soundtrack_id>', methods=["PUT"])
def update_soundtrack(str_soundtrack_id: str):
    if not SoundtracksPutValidator().validate(request.json):
        abort(400)

    soundtrack_repository = SoundtrackMysqlRepository()
    soundtrack_id = SoundtrackId.from_string(str_soundtrack_id)
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
    chapter_repository = ChapterMysqlRepository()
    soundtrack_id = SoundtrackId.from_string(str_soundtrack_id)
    
    try:
        DeleteSoundtrack(soundtrack_repository, chapter_repository).run(soundtrack_id)
    except Exception as error:
        if isinstance(error, UnexistingSoundtrackError):
            abort(404)
        else:
            abort(500)

    return ('', 204)


@soundtracks.route('/like', methods=["POST"])
def like_soundtrack():
    soundtrack_repository = SoundtrackMysqlRepository()

    if not SoundtracksLikePostValidator().validate(request.json):
        abort(400)
    
    user_id = UserId.from_string(request.json['user_id'])
    soundtrack_id = SoundtrackId.from_string(request.json['soundtrack_id'])

    try:
        LikeSoundtrack(soundtrack_repository).run(user_id, soundtrack_id)
    except Exception as error:
        if isinstance(error, AlreadyLikedSoundtrackError):
            abort(409)
        else:
            abort(500)

    return 200
