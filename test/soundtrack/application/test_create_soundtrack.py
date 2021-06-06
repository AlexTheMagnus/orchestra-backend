import pytest
import uuid
from faker import Faker

from test.soundtrack.infrastructure.soundtrack_in_memory_repository import SoundtrackInMemoryRepository
from src.soundtrack.application.create_soundtrack import CreateSoundtrack
from src.soundtrack.domain.soundtrack_id import SoundtrackId
from src.soundtrack.domain.isbn_13 import Isbn13
from src.soundtrack.domain.soundtrack_title import SoundtrackTitle
from src.soundtrack.domain.user_id import UserId
from src.soundtrack.domain.chapter.chapter import Chapter
from src.soundtrack.domain.soundtrack import Soundtrack
from test.soundtrack.builder.soundtrack_builder import SoundtrackBuilder
from src.soundtrack.domain.exceptions.already_existing_soundtrack_error import AlreadyExistingSoundtrackError

fake = Faker()

soundtrack_repository = SoundtrackInMemoryRepository()
use_case: CreateSoundtrack = CreateSoundtrack(soundtrack_repository)
soundtrack_id: SoundtrackId = SoundtrackId.from_string(str(uuid.uuid4()))
book: Isbn13 = Isbn13.from_string("978-2-1550-9533-9")
soundtrack_title = SoundtrackTitle.from_string(fake.pystr())
author: UserId = UserId.from_string(fake.pystr())
chapters: list[Chapter] = []


class TestCreateSoundtrack():

    def test_new_soundtrack_is_created(self):
        soundtrack: Soundtrack = SoundtrackBuilder().with_soundtrack_id(
            soundtrack_id).with_book(book).with_soundtrack_title(soundtrack_title).with_author(
                author).with_chapters(chapters).build()

        use_case.run(soundtrack)

        found_soundtrack: Soundtrack = soundtrack_repository.find(
            soundtrack_id)
        assert found_soundtrack != None
        assert found_soundtrack.soundtrack_id.value == soundtrack_id.value
        assert found_soundtrack.book.value == book.value
        assert found_soundtrack.soundtrack_title.value == soundtrack_title.value
        assert found_soundtrack.author.value == author.value
        assert found_soundtrack.chapters == chapters

    def test_already_existing_soundtrack_throws_an_error(self):
        soundtrack: Soundtrack = SoundtrackBuilder(
        ).with_soundtrack_id(soundtrack_id).build()

        with pytest.raises(AlreadyExistingSoundtrackError):
            use_case.run(soundtrack)
