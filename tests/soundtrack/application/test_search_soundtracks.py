from faker import Faker
from typing import List
import uuid

from ..builder.soundtrack_builder import SoundtrackBuilder
from ..infrastructure.soundtrack_in_memory_repository import SoundtrackInMemoryRepository
from src.soundtrack.application.search_soundtracks import SearchSoundtracks
from src.soundtrack.domain.isbn_13 import Isbn13
from src.soundtrack.domain.user_id import UserId

fake = Faker()
soundtrack_repository = SoundtrackInMemoryRepository()
use_case = SearchSoundtracks(soundtrack_repository)

class TestSearchSoundtracks():
    def test_search_results_are_ordered_by_number_of_likes(self):
        isbn13 = Isbn13.from_string('978-7-1742-5750-8')

        most_liked_soundtrack = SoundtrackBuilder().with_book(isbn13).build()
        soundtrack_repository.save(most_liked_soundtrack)
        for x in range(2):
            user_id = UserId.from_string(str(uuid.uuid4()))
            soundtrack_repository.save_like(user_id, most_liked_soundtrack.soundtrack_id)

        liked_soundtrack = SoundtrackBuilder().with_book(isbn13).build()
        soundtrack_repository.save(liked_soundtrack)
        user_id = UserId.from_string(str(uuid.uuid4()))
        soundtrack_repository.save_like(user_id, liked_soundtrack.soundtrack_id)

        no_liked_soundtrack = SoundtrackBuilder().with_book(isbn13).build()
        soundtrack_repository.save(no_liked_soundtrack)

        search_results: List[Soundtrack] = use_case.run({"book": isbn13})
        assert search_results == [most_liked_soundtrack, liked_soundtrack, no_liked_soundtrack]

    def test_search_returns_a_maximum_number_of_twenty_results(self):
        isbn13 = Isbn13.from_string('978-8-3653-8896-4')

        for x in range(fake.random_number(2, True) + 21):
            soundtrack = SoundtrackBuilder().with_book(isbn13).build()
            soundtrack_repository.save(soundtrack)

        search_results: List[Soundtrack] = use_case.run({"book": isbn13})
        assert len(search_results) == 20

    def test_search_returns_empty_array_when_no_results(self):
        isbn13 = Isbn13.from_string('978-1-4696-2919-3')

        search_results: List[Soundtrack] = use_case.run({"book": isbn13})
        assert search_results == []