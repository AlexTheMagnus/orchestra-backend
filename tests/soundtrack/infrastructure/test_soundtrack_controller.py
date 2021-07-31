import pytest
import json
import uuid

from faker import Faker

from orchestra import app
from src.soundtrack.infrastructure.soundtrack_mysql_repository import SoundtrackMysqlRepository
from src.soundtrack.domain.soundtrack_id import SoundtrackId
from src.soundtrack.domain.user_id import UserId
from ..builder.soundtrack_builder import SoundtrackBuilder

fake = Faker()
soundtrack_repository = SoundtrackMysqlRepository()


def teardown_module():
    SoundtrackMysqlRepository().clean()


class TestSoundtrackPostController():
    def test_should_create_and_save_a_soundtrack_with_the_passed_parameters(self):
        soundtrack_id = SoundtrackId.from_string(str(uuid.uuid4()))
        soundtracks_post_request_params = get_soundtrack_post_request_params_with_id(
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

        soundtracks_post_request_params = get_soundtrack_post_request_params_with_id(
            soundtrack_id.value)

        response = app.test_client().post(
            '/soundtracks',
            data=json.dumps(soundtracks_post_request_params),
            content_type='application/json'
        )

        assert response.status_code == 409


def get_soundtrack_post_request_params_with_id(soundtrack_id: str):
    return {
        "soundtrack_id": soundtrack_id,
        "book": "978-2-1550-9533-9",
        "soundtrack_title": fake.pystr(),
        "author": str(uuid.uuid4())
    }


class TestSoundtrackGetController():
    def test_should_return_the_user_soundtracks(self):
        author: UserId = UserId.from_string(fake.pystr())
        soundtracks_get_request_params = get_soundtrack_get_request_params_with_id(author.value)

        for x in range(3):
            soundtrack: Soundtrack = SoundtrackBuilder().with_author(author).build()
            soundtrack_repository.save(soundtrack)

        response = app.test_client().get(
            '/soundtracks/user/{0}',
            data=json.dumps(soundtracks_get_request_params),
            content_type='application/json'
        )

        assert response.status_code == 200
        data = json.loads(response.get_data(as_text=True))
        assert len(data["soundtracks_list"]) == 3

def get_soundtrack_get_request_params_with_id(author: str):
    return {
        "author": author
    }
