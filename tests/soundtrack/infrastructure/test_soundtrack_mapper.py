import pytest

from src.soundtrack.domain.soundtrack import Soundtrack
from src.soundtrack.infrastructure.soundtrack_mapper import SoundtrackMapper
from src.soundtrack.infrastructure.soundtrack_dto import SoundtrackDTO
from ..builder.soundtrack_builder import SoundtrackBuilder


class TestSoundtrackMapper:

    def test_soundtrack_aggregate_from_soundtrack_dto_has_same_attributes(self):
        soundtrack_dto: SoundtrackDTO = SoundtrackBuilder().build_dto()

        soundtrack: Soundtrack = SoundtrackMapper().from_dto_to_aggregate(soundtrack_dto)

        assert soundtrack_dto['soundtrack_id'] == soundtrack.soundtrack_id.value
        assert soundtrack_dto['book'] == soundtrack.book.value
        assert soundtrack_dto['soundtrack_title'] == soundtrack.soundtrack_title.value
        assert soundtrack_dto['author'] == soundtrack.author.value
        assert soundtrack_dto['chapters'] == soundtrack.chapters

    def test_soundtrack_dto_from_soundtrack_aggregate_has_same_attributes(self):
        soundtrack: Soundtrack = SoundtrackBuilder().build()

        soundtrack_dto: SoundtrackDTO = SoundtrackMapper().from_aggregate_to_dto(soundtrack)

        assert soundtrack_dto['soundtrack_id'] == soundtrack.soundtrack_id.value
        assert soundtrack_dto['book'] == soundtrack.book.value
        assert soundtrack_dto['soundtrack_title'] == soundtrack.soundtrack_title.value
        assert soundtrack_dto['author'] == soundtrack.author.value
        assert soundtrack_dto['chapters'] == soundtrack.chapters
