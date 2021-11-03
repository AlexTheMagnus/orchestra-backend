from flask import Blueprint, abort, jsonify, request

from .chapter_mysql_repository import ChapterMysqlRepository
from ..soundtrack_mysql_repository import SoundtrackMysqlRepository
from .validators.chapters_post_validator import ChaptersPostValidator
from ...domain.chapter.chapter import Chapter
from ...domain.chapter.chapter_id import ChapterId
from ...domain.soundtrack_id import SoundtrackId
from ...domain.chapter.chapter_number import ChapterNumber
from ...domain.chapter.theme import Theme
from ...domain.chapter.chapter_title import ChapterTitle
from ...application.chapter.add_chapter import AddChapter
from ...domain.chapter.exceptions.already_existing_chapter_error import AlreadyExistingChapterError
from ...domain.exceptions.unexisting_soundtrack_error import UnexistingSoundtrackError
from ...application.chapter.get_soundtrack_chapters import GetSoundtrackChapters
from .from_chapter_to_dict import FromChapterToDict

chapters = Blueprint("chapters", __name__, url_prefix="/chapters")

@chapters.route('', methods=["POST"])
def add_chapter():
    chapter_repository = ChapterMysqlRepository()
    soundtrack_repository = SoundtrackMysqlRepository()

    if not ChaptersPostValidator().validate(request.json):
        abort(400)

    chapter = Chapter(
        chapter_id=ChapterId.from_string(request.json['chapter_id']),
        soundtrack_id=SoundtrackId.from_string(request.json['soundtrack_id']),
        chapter_number=ChapterNumber.from_integer(request.json['chapter_number']),
        theme=Theme.from_string(request.json['theme']),
        chapter_title=ChapterTitle.from_string(request.json['chapter_title']),
    )

    try:
        AddChapter(chapter_repository, soundtrack_repository).run(chapter)
    except Exception as error:
        if isinstance(error, AlreadyExistingChapterError):
            abort(409)
        if isinstance(error, UnexistingSoundtrackError):
            abort(404)
        else:
            abort(500)

    return '200'


@chapters.route('/soundtrack/<string:str_soundtrack_id>', methods=["GET"])
def get_soundtrack_chapters(str_soundtrack_id: str):
    chapter_repository = ChapterMysqlRepository()
    soundtrack_id = SoundtrackId.from_string(str_soundtrack_id)

    try:
        chapters_list = GetSoundtrackChapters(chapter_repository).run(soundtrack_id)
    except Exception as error:
        abort(500)

    return jsonify(FromChapterToDict.with_chapters_list(chapters_list)), '200'