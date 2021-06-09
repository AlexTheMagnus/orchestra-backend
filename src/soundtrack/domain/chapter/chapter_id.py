from uuid import UUID

from .exceptions.not_a_valid_chapter_id_error import NotAValidChapterIdError


class ChapterId():
    def __init__(self, chapter_id: str):
        self.__validate_uuid_v4_format(chapter_id)
        self.__value: str = chapter_id

    @staticmethod
    def from_string(chapter_id: str):
        return ChapterId(chapter_id)

    @property
    def value(self):
        return self.__value

    def __validate_uuid_v4_format(self, chapter_id: str):
        uuid_chapter_id = UUID(chapter_id)
        if uuid_chapter_id.version != 4:
            raise(NotAValidChapterIdError(uuid_chapter_id))
