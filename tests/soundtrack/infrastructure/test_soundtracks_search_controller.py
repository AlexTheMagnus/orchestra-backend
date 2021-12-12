import json
import uuid
from faker import Faker

from ..builder.soundtrack_builder import SoundtrackBuilder
from orchestra import app
from src.soundtrack.domain.isbn_13 import Isbn13
from src.soundtrack.domain.user_id import UserId
from src.soundtrack.infrastructure.from_soundtrack_to_dict import FromSoundtrackToDict
from src.soundtrack.infrastructure.soundtrack_mysql_repository import SoundtrackMysqlRepository
from src.user.infrastructure.user_mysql_repository import UserMysqlRepository

fake = Faker()
soundtrack_repository = SoundtrackMysqlRepository()
user_repository = UserMysqlRepository()

def teardown_module():
    soundtrack_repository.clean()
    user_repository.clean()

class TestSoundtracksSearchPostController():
    def test_should_create_and_return_a_search_with_the_passed_parameters_ordered_by_number_of_likes(self):
        isbn13 = Isbn13.from_string('978-1-5123-9891-5')

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

        response = app.test_client().post(
            '/soundtracks/search',
            data=json.dumps(get_soundtracks_search_request_params_with_book(isbn13.value)),
            content_type='application/json'
        )

        assert response.status_code == 200
        response_data = json.loads(response.get_data(as_text=True))
        assert response_data != None
        assert response_data['soundtracks_list'] == FromSoundtrackToDict.with_soundtracks_list([most_liked_soundtrack, liked_soundtrack, no_liked_soundtrack])['soundtracks_list']

    def test_should_return_a_maximum_number_of_twenty_results(self):
        isbn13 = Isbn13.from_string('978-3-6190-0929-9')

        for x in range(fake.random_number(2, True) + 21):
            soundtrack = SoundtrackBuilder().with_book(isbn13).build()
            soundtrack_repository.save(soundtrack)

        response = app.test_client().post(
            '/soundtracks/search',
            data=json.dumps(get_soundtracks_search_request_params_with_book(isbn13.value)),
            content_type='application/json'
        )

        assert response.status_code == 200
        response_data = json.loads(response.get_data(as_text=True))
        assert response_data != None
        assert len(response_data['soundtracks_list']) == 20

    def test_should_return_empty_array_when_there_are_no_results(self):
        isbn13 = Isbn13.from_string('978-1-0731-4231-6')

        response = app.test_client().post(
            '/soundtracks/search',
            data=json.dumps(get_soundtracks_search_request_params_with_book(isbn13.value)),
            content_type='application/json'
        )

        assert response.status_code == 200
        response_data = json.loads(response.get_data(as_text=True))
        assert response_data != None
        assert response_data['soundtracks_list'] == []

def get_soundtracks_search_request_params_with_book(book: str):
    return {
        "book": book
    }