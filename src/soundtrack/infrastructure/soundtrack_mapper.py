from src.soundtrack.domain.soundtrack_id import SoundtrackId
from src.soundtrack.domain.isbn_13 import Isbn13
from src.soundtrack.domain.soundtrack_title import SoundtrackTitle
from src.soundtrack.domain.user_id import UserId
from src.soundtrack.domain.chapter.chapter import Chapter
from src.soundtrack.domain.soundtrack import Soundtrack
from src.soundtrack.infrastructure.soundtrack_dto import SoundtrackDTO


class SoundtrackMapper:
    @staticmethod
    def from_dto_to_aggregate(soundtrack_dto: SoundtrackDTO) -> Soundtrack:
        return Soundtrack(
            soundtrack_id=SoundtrackId.from_string(
                soundtrack_dto['soundtrack_id']),
            book=Isbn13.from_string(
                soundtrack_dto['book']),
            soundtrack_title=SoundtrackTitle.from_string(
                soundtrack_dto['soundtrack_title']),
            author=UserId.from_string(soundtrack_dto['author']),
            chapters=soundtrack_dto['chapters']
        )

    @staticmethod
    def from_aggregate_to_dto(soundtrack: Soundtrack) -> SoundtrackDTO:
        return SoundtrackDTO(
            soundtrack_id=soundtrack.soundtrack_id.value,
            book=soundtrack.book.value,
            soundtrack_title=soundtrack.soundtrack_title.value,
            author=soundtrack.author.value,
            chapters=soundtrack.chapters
        )
