from src.soundtrack.domain.soundtrack_id import SoundtrackId
from src.soundtrack.domain.isbn_13 import Isbn13
from src.soundtrack.domain.user_id import UserId
from src.soundtrack.domain.chapter.chapter import Chapter
from src.soundtrack.domain.Soundtrack import Soundtrack
from src.soundtrack.infrastructure.soundtrack_dto import SoundtrackDTO


class SoundtrackMapper:
    @staticmethod
    def from_dto_to_aggregate(soundtrack_dto: SoundtrackDTO) -> Soundtrack:
        return Soundtrack(
            soundtrack_id=SoundtrackId.from_string(
                soundtrack_dto['soundtrack_id']),
            username=soundtrack_dto['username'],
            user_id=UserId.from_string(soundtrack_dto['user_id']),
            password=Password.from_string(soundtrack_dto['password'])
        )

    @staticmethod
    def from_aggregate_to_dto(soundtrack: Soundtrack) -> SoundtrackDTO:
        return SoundtrackDTO(
            user_id=soundtrack.user_id.value,
            email=soundtrack.email,
            password=soundtrack.password.value,
            username=soundtrack.username,
            profile_picture=soundtrack.profile_picture,
            first_name=soundtrack.first_name,
            last_name=soundtrack.last_name,
            country=soundtrack.country,
            city=soundtrack.city
        )
