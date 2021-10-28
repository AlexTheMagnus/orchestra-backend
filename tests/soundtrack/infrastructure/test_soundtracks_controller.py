import json
import uuid
from faker import Faker

from orchestra import app
from src.soundtrack.infrastructure.soundtrack_mysql_repository import SoundtrackMysqlRepository
from src.soundtrack.infrastructure.chapter.chapter_mysql_repository import ChapterMysqlRepository
from src.soundtrack.domain.soundtrack_id import SoundtrackId
from src.soundtrack.domain.soundtrack import Soundtrack
from src.soundtrack.domain.user_id import UserId
from ..builder.soundtrack_builder import SoundtrackBuilder

fake = Faker()
soundtrack_repository = SoundtrackMysqlRepository()
chapter_repository = ChapterMysqlRepository()

def teardown_module():
    chapter_repository.clean()
    soundtrack_repository.clean()

class TestSoundtracksPostController():
    def test_should_create_and_save_a_soundtrack_with_the_passed_parameters(self):
        soundtrack_id = SoundtrackId.from_string(str(uuid.uuid4()))
        soundtracks_post_request_params = get_soundtracks_post_request_params_with_id(
            soundtrack_id.value)

        response = app.test_client().post(
            '/soundtracks',
            data=json.dumps(soundtracks_post_request_params),
            content_type='application/json'
        )

        saved_soundtrack = soundtrack_repository.find(soundtrack_id)
        assert response.status_code == 200
        assert saved_soundtrack != None
        assert saved_soundtrack.soundtrack_id.value == soundtracks_post_request_params[
            "soundtrack_id"]
        assert saved_soundtrack.book.value == soundtracks_post_request_params["book"]
        assert saved_soundtrack.soundtrack_title.value == soundtracks_post_request_params[
            "soundtrack_title"]
        assert saved_soundtrack.author.value == soundtracks_post_request_params["author"]

    def test_should_return_409_when_creating_a_soundtrack_with_an_already_registered_soundtrack_id(self):
        soundtrack_id = SoundtrackId.from_string(str(uuid.uuid4()))
        soundtrack = SoundtrackBuilder().with_soundtrack_id(soundtrack_id).build()
        soundtrack_repository.save(soundtrack)

        soundtracks_post_request_params = get_soundtracks_post_request_params_with_id(
            soundtrack_id.value)

        response = app.test_client().post(
            '/soundtracks',
            data=json.dumps(soundtracks_post_request_params),
            content_type='application/json'
        )

        assert response.status_code == 409


def get_soundtracks_post_request_params_with_id(soundtrack_id: str):
    return {
        "soundtrack_id": soundtrack_id,
        "book": "978-2-1550-9533-9",
        "soundtrack_title": fake.pystr(),
        "author": str(uuid.uuid4())
    }


class TestSoundtracksGetController():
    def test_should_return_the_user_soundtracks(self):
        author: UserId = UserId.from_string(str(uuid.uuid4()))

        for x in range(3):
            soundtrack: Soundtrack = SoundtrackBuilder().with_author(author).build()
            soundtrack_repository.save(soundtrack)

        response = app.test_client().get(
            '/soundtracks/user/{0}'.format(author.value),
            content_type='application/json'
        )

        assert response.status_code == 200
        data = json.loads(response.get_data(as_text=True))
        assert len(data["soundtracks_list"]) == 3

    def test_should_return_a_soundtrack_by_id(self):
        soundtrack_id: SoundtrackId = SoundtrackId.from_string(str(uuid.uuid4()))
        soundtrack: Soundtrack = SoundtrackBuilder().with_soundtrack_id(soundtrack_id).build()
        soundtrack_repository.save(soundtrack)

        response = app.test_client().get(
            '/soundtracks/{0}'.format(soundtrack_id.value),
            content_type='application/json'
        )

        assert response.status_code == 200
        data = json.loads(response.get_data(as_text=True))
        assert data['soundtrack_id'] == soundtrack.soundtrack_id.value
        assert data['book'] == soundtrack.book.value
        assert data['soundtrack_title'] == soundtrack.soundtrack_title.value
        assert data['author'] == soundtrack.author.value

    def test_should_return_404_when_asking_for_an_unexisting_soundtrack_id(self):
        str_soundtrack_id: string = str(uuid.uuid4())

        response = app.test_client().get(
            '/soundtracks/{0}'.format(str_soundtrack_id),
            content_type='application/json'
        )

        assert response.status_code == 404


class TestSoundtracksPutController():
    def test_should_update_a_soundtrack_with_the_passed_parameters(self):
            soundtrack: Soundtrack = SoundtrackBuilder().build()
            soundtrack_repository.save(soundtrack)
            soundtracks_put_request_params = get_soundtracks_put_request_params_with_id()

            response = app.test_client().put(
                '/soundtracks/update/{0}'.format(soundtrack.soundtrack_id.value),
                data=json.dumps(soundtracks_put_request_params),
                content_type='application/json'
            )
            
            saved_soundtrack = soundtrack_repository.find(soundtrack.soundtrack_id)
            assert response.status_code == 200
            assert saved_soundtrack != None
            assert saved_soundtrack.soundtrack_id.value == soundtrack.soundtrack_id.value
            assert saved_soundtrack.book.value == soundtracks_put_request_params["book"]
            assert saved_soundtrack.soundtrack_title.value == soundtracks_put_request_params[
                "soundtrack_title"]
            assert saved_soundtrack.author.value == soundtrack.author.value

    def test_should_update_a_soundtrack_book(self):
            soundtrack: Soundtrack = SoundtrackBuilder().build()
            soundtrack_repository.save(soundtrack)
            soundtracks_put_request_params = {"book": "0-6103-1972-8"}

            response = app.test_client().put(
                '/soundtracks/update/{0}'.format(soundtrack.soundtrack_id.value),
                data=json.dumps(soundtracks_put_request_params),
                content_type='application/json'
            )
            
            saved_soundtrack = soundtrack_repository.find(soundtrack.soundtrack_id)
            assert response.status_code == 200
            assert saved_soundtrack != None
            assert saved_soundtrack.soundtrack_id.value == soundtrack.soundtrack_id.value
            assert saved_soundtrack.book.value == soundtracks_put_request_params["book"]
            assert saved_soundtrack.soundtrack_title.value == soundtrack.soundtrack_title.value
            assert saved_soundtrack.author.value == soundtrack.author.value

    def test_should_update_a_soundtrack_title(self):
            soundtrack: Soundtrack = SoundtrackBuilder().build()
            soundtrack_repository.save(soundtrack)
            soundtracks_put_request_params = {"soundtrack_title": fake.pystr()}

            response = app.test_client().put(
                '/soundtracks/update/{0}'.format(soundtrack.soundtrack_id.value),
                data=json.dumps(soundtracks_put_request_params),
                content_type='application/json'
            )
            
            saved_soundtrack = soundtrack_repository.find(soundtrack.soundtrack_id)
            assert response.status_code == 200
            assert saved_soundtrack != None
            assert saved_soundtrack.soundtrack_id.value == soundtrack.soundtrack_id.value
            assert saved_soundtrack.book.value == soundtrack.book.value
            assert saved_soundtrack.soundtrack_title.value == soundtracks_put_request_params[
                "soundtrack_title"]
            assert saved_soundtrack.author.value == soundtrack.author.value

    def test_should_return_404_when_the_soundtrack_to_be_updated_does_not_exist(self):
        non_existing_soundtrack_id = SoundtrackId.from_string(str(uuid.uuid4()))
        soundtracks_put_request_params = get_soundtracks_put_request_params_with_id()

        response = app.test_client().put(
            '/soundtracks/update/{0}'.format(non_existing_soundtrack_id.value),
            data=json.dumps(soundtracks_put_request_params),
            content_type='application/json'
        )

        assert response.status_code == 404

def get_soundtracks_put_request_params_with_id():
    return {
        "book": "0-6103-1972-8",
        "soundtrack_title": fake.pystr()
    }