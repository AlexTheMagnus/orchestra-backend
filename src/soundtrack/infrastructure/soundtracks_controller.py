from flask import Blueprint, abort, request
from typing import List

from .soundtrack_mysql_repository import SoundtrackMysqlRepository
from ..application.create_soundtrack import CreateSoundtrack
from ..domain.soundtrack import Soundtrack
from ..domain.soundtrack_id import SoundtrackId
from ..domain.isbn_13 import Isbn13
from ..domain.soundtrack_title import SoundtrackTitle
from ..domain.user_id import UserId
from ..domain.chapter.chapter import Chapter
from ..domain.exceptions.already_existing_soundtrack_error import AlreadyExistingSoundtrackError
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
