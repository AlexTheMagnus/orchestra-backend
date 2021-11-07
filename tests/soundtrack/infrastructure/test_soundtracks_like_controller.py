import json
import uuid
from typing import List

from orchestra import app
from src.soundtrack.domain.soundtrack import Soundtrack
from src.soundtrack.domain.user_id import UserId
from src.soundtrack.infrastructure.soundtrack_mysql_repository import SoundtrackMysqlRepository
from ..builder.soundtrack_builder import SoundtrackBuilder

soundtrack_repository = SoundtrackMysqlRepository()

def teardown_module():
    soundtrack_repository.clean()

class TestSoundtracksLikePostController():
    def test_should_like_a_soundtrack(self):
        user_id = UserId.from_string(str(uuid.uuid4()))
        soundtrack: Soundtrack = SoundtrackBuilder().build()
        soundtrack_repository.save(soundtrack)

        soundtracks_like_post_request_params = {
            "user_id": user_id.value,
            "soundtrack_id": soundtrack.soundtrack_id.value
        }

        response = app.test_client().post(
            '/soundtracks/like',
            data=json.dumps(soundtracks_like_post_request_params),
            content_type='application/json'
        )

        saved_likes: List[UserId] = soundtrack_repository.get_likes(soundtrack.soundtrack_id)
        assert response.status_code == 200
        assert saved_likes != None
        assert len(saved_likes) == 1
        assert saved_likes[0].value == soundtracks_like_post_request_params["user_id"]

    def test_should_return_404_when_liking_an_unexisting_soundtrack(self):
        user_id = UserId.from_string(str(uuid.uuid4()))
        soundtrack: Soundtrack = SoundtrackBuilder().build()

        soundtracks_like_post_request_params = {
            "user_id": user_id.value,
            "soundtrack_id": soundtrack.soundtrack_id.value
        }

        response = app.test_client().post(
            '/soundtracks/like',
            data=json.dumps(soundtracks_like_post_request_params),
            content_type='application/json'
        )

        assert response.status_code == 404

    def test_should_return_409_when_linke_already_exists(self):
        user_id = UserId.from_string(str(uuid.uuid4()))
        soundtrack: Soundtrack = SoundtrackBuilder().build()
        soundtrack_repository.save(soundtrack)
        soundtrack_repository.save_like(user_id, soundtrack.soundtrack_id)

        soundtracks_like_post_request_params = {
            "user_id": user_id.value,
            "soundtrack_id": soundtrack.soundtrack_id.value
        }

        response = app.test_client().post(
            '/soundtracks/like',
            data=json.dumps(soundtracks_like_post_request_params),
            content_type='application/json'
        )

        assert response.status_code == 409
        

class TestSoundtracksLikeGetController():
    def test_should_return_the_users_who_liked_a_soundtrack(self):
        soundtrack: Soundtrack = SoundtrackBuilder().build()
        soundtrack_repository.save(soundtrack)
        users: List[UserId] = []

        for x in range(3):
            users.append(UserId.from_string(str(uuid.uuid4())))
            soundtrack_repository.save_like(users[x], soundtrack.soundtrack_id)

        response = app.test_client().get(
            '/soundtracks/{0}/likes'.format(soundtrack.soundtrack_id.value),
            content_type='application/json'
        )

        saved_likes: List[UserId] = soundtrack_repository.get_likes(soundtrack.soundtrack_id)
        assert response.status_code == 200
        assert saved_likes != None
        assert len(saved_likes) == 3
        str_users = [user.value for user in users]
        str_saved_likes = [like.value for like in saved_likes]
        assert set(str_users) == set(str_saved_likes)