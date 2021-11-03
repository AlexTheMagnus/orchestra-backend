from faker import Faker

from ..infrastructure.soundtrack_in_memory_repository import SoundtrackInMemoryRepository
from src.soundtrack.domain.soundtrack_title import SoundtrackTitle
from src.soundtrack.domain.isbn_13 import Isbn13
from src.soundtrack.application.update_soundtrack import UpdateSoundtrack
from ..builder.soundtrack_builder import SoundtrackBuilder

fake = Faker()

soundtrack_repository = SoundtrackInMemoryRepository()
use_case: UpdateSoundtrack = UpdateSoundtrack(soundtrack_repository)


class TestUpdateSoundtrack():
    def test_soundtrack_title_is_updated(self):
        soundtrack: Soundtrack = SoundtrackBuilder().build()
        soundtrack_repository.save(soundtrack)

        new_soundtrack_title: SoundtrackTitle = SoundtrackTitle.from_string(fake.pystr())
        use_case.run(soundtrack.soundtrack_id, {'book': None, 'soundtrack_title': new_soundtrack_title})

        found_soundtrack: Soundtrack = soundtrack_repository.find(
        soundtrack.soundtrack_id)
        assert found_soundtrack != None
        assert found_soundtrack.soundtrack_id.value == soundtrack.soundtrack_id.value
        assert found_soundtrack.book.value == soundtrack.book.value
        assert found_soundtrack.soundtrack_title.value == new_soundtrack_title.value
        assert found_soundtrack.author.value == soundtrack.author.value

    def test_soundtrack_book_is_updated(self):
        soundtrack: Soundtrack = SoundtrackBuilder().build()
        soundtrack_repository.save(soundtrack)

        new_soundtrack_book: Isbn13 = Isbn13.from_string('0-2045-5150-1')
        use_case.run(soundtrack.soundtrack_id, {'book': new_soundtrack_book, 'soundtrack_title': None})

        found_soundtrack: Soundtrack = soundtrack_repository.find(
        soundtrack.soundtrack_id)
        assert found_soundtrack != None
        assert found_soundtrack.soundtrack_id.value == soundtrack.soundtrack_id.value
        assert found_soundtrack.book.value == new_soundtrack_book.value
        assert found_soundtrack.soundtrack_title.value == soundtrack.soundtrack_title.value
        assert found_soundtrack.author.value == soundtrack.author.value
