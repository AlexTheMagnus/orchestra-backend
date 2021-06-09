from uuid import UUID

from .exceptions.not_a_valid_soundtrack_id_error import NotAValidSoundtrackIdError


class SoundtrackId():

    def __init__(self, soundtrack_id: str):
        self.__validate_uuid_v4_format(soundtrack_id)
        self.__value: str = soundtrack_id

    @staticmethod
    def from_string(soundtrack_id: str):
        return SoundtrackId(soundtrack_id)

    @property
    def value(self):
        return self.__value

    def __validate_uuid_v4_format(self, soundtrack_id: str):
        uuid_soundtrack_id = UUID(soundtrack_id)
        if uuid_soundtrack_id.version != 4:
            raise(NotAValidSoundtrackIdError(uuid_soundtrack_id))
