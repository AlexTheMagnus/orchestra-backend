from faker import Faker

from ..infrastructure.soundtrack_in_memory_repository import SoundtrackInMemoryRepository
from src.soundtrack.domain.soundtrack_title import SoundtrackTitle
from src.soundtrack.domain.isbn_13 import Isbn13
from src.soundtrack.application.edit_soundtrack import EditSoundtrack
from ..builder.soundtrack_builder import SoundtrackBuilder

fake = Faker()

soundtrack_repository = SoundtrackInMemoryRepository()
use_case: EditSoundtrack = EditSoundtrack(soundtrack_repository)


class TestEditSoundtrack():
    def test_soundtrack_title_is_edited(self):
        soundtrack: Soundtrack = SoundtrackBuilder().build()
        soundtrack_repository.save(soundtrack)

        new_soundtrack_title: SoundtrackTitle = SoundtrackTitle.from_string(fake.pystr())
        soundtrack_with_new_title: Soundtrack = SoundtrackBuilder().with_soundtrack_id(
            soundtrack.soundtrack_id).with_author(soundtrack.author).with_book(
            soundtrack.book).with_soundtrack_title(new_soundtrack_title).build()
        use_case.run(soundtrack_with_new_title)

        found_soundtrack: Soundtrack = soundtrack_repository.find(
        soundtrack.soundtrack_id)
        assert found_soundtrack != None
        assert found_soundtrack.soundtrack_id.value == soundtrack.soundtrack_id.value
        assert found_soundtrack.book.value == soundtrack.book.value
        assert found_soundtrack.soundtrack_title.value == new_soundtrack_title.value
        assert found_soundtrack.author.value == soundtrack.author.value

    def test_soundtrack_book_is_edited(self):
        soundtrack: Soundtrack = SoundtrackBuilder().build()
        soundtrack_repository.save(soundtrack)

        new_soundtrack_book: Isbn13 = Isbn13.from_string('0-2045-5150-1')
        soundtrack_with_new_title: Soundtrack = SoundtrackBuilder().with_soundtrack_id(
            soundtrack.soundtrack_id).with_author(soundtrack.author).with_book(
            new_soundtrack_book).with_soundtrack_title(soundtrack.soundtrack_title).build()
        use_case.run(soundtrack_with_new_title)

        found_soundtrack: Soundtrack = soundtrack_repository.find(
        soundtrack.soundtrack_id)
        assert found_soundtrack != None
        assert found_soundtrack.soundtrack_id.value == soundtrack.soundtrack_id.value
        assert found_soundtrack.book.value == new_soundtrack_book.value
        assert found_soundtrack.soundtrack_title.value == soundtrack.soundtrack_title.value
        assert found_soundtrack.author.value == soundtrack.author.value
