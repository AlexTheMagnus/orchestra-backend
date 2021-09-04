from flask import Blueprint, abort, jsonify, request

from typing import List

from .soundtrack_mysql_repository import SoundtrackMysqlRepository
from ..application.create_soundtrack import CreateSoundtrack
from ..application.get_user_soundtracks import GetUserSoundtracks
from ..application.get_soundtrack_by_id import GetSoundtrackById
from ..domain.soundtrack import Soundtrack
from ..domain.soundtrack_id import SoundtrackId
from ..domain.isbn_13 import Isbn13
from ..domain.soundtrack_title import SoundtrackTitle
from ..domain.user_id import UserId
from ..domain.chapter.chapter import Chapter
from ..domain.exceptions.already_existing_soundtrack_error import AlreadyExistingSoundtrackError
from ..domain.exceptions.unexisting_soundtrack_error import UnexistingSoundtrackError
from .from_soundtrack_to_dict import FromSoundtrackToDict
from .validators.soundtracks_post_validator import SoundtracksPostValidator

soundtracks = Blueprint("soundtracks", __name__, url_prefix="/soundtracks")


@soundtracks.route('', methods=["POST"])
def create_soundtrack():
    soundtrack_repository = SoundtrackMysqlRepository()

    if not SoundtracksPostValidator().validate(request.json):
        abort(400)

    chapters = List[Chapter]

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
