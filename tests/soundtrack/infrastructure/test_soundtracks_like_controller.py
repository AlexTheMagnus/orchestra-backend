import json
import uuid
from typing import List

from orchestra import app
from src.soundtrack.domain.soundtrack_id import SoundtrackId
from src.soundtrack.domain.user_id import UserId
from src.soundtrack.infrastructure.soundtrack_mysql_repository import SoundtrackMysqlRepository

soundtrack_repository = SoundtrackMysqlRepository()

def teardown_module():
    soundtrack_repository.clean()

class TestSoundtracksLikePostController():
    def test_should_like_a_soundtrack(self):
        user_id = UserId.from_string(str(uuid.uuid4()))
        soundtrack_id = SoundtrackId.from_string(str(uuid.uuid4()))

        soundtracks_like_post_request_params = {
            "user_id": user_id.value,
            "soundtrack_id": soundtrack_id.value
        }

        response = app.test_client().post(
            '/soundtracks/like',
            data=json.dumps(soundtracks_like_post_request_params),
            content_type='application/json'
        )

        saved_likes: List[UserId] = soundtrack_repository.get_likes(soundtrack_id)
        assert response.status_code == 200
        assert saved_likes != None
        assert saved_likes == [soundtracks_like_post_request_params["user_id"]]