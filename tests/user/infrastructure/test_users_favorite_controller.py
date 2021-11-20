from typing import List
import json
import uuid

from ...soundtrack.builder.soundtrack_builder import SoundtrackBuilder
from ..builder.user_builder import UserBuilder
from orchestra import app
from src.soundtrack.domain.soundtrack_id import SoundtrackId
from src.soundtrack.infrastructure.soundtrack_mysql_repository import SoundtrackMysqlRepository
from src.user.domain.user_id import UserId
from src.user.infrastructure.user_mysql_repository import UserMysqlRepository

user_repository = UserMysqlRepository()
soundtrack_repository = SoundtrackMysqlRepository()

def teardown_module():
    user_repository.clean()
    soundtrack_repository.clean()

class TestUsersFavoritePostController():
  def test_should_add_a_soundtrack_to_favorites(self):
        user = UserBuilder().build()
        user_repository.save(user)
        soundtrack = SoundtrackBuilder().build()
        soundtrack_repository.save(soundtrack)

        users_favorite_post_request_params = {
            "user_id": user.user_id.value,
            "soundtrack_id": soundtrack.soundtrack_id.value
        }

        response = app.test_client().post(
            '/users/favorite',
            data=json.dumps(users_favorite_post_request_params),
            content_type='application/json'
        )

        saved_favorites: List[SoundtrackId] = user_repository.get_favorites(user.user_id)
        assert response.status_code == 200
        assert saved_favorites != None
        assert len(saved_favorites) == 1
        assert saved_favorites[0].value == users_favorite_post_request_params["soundtrack_id"]

  def test_should_return_404_when_adding_a_soundtrack_to_unexisting_user_favorites(self):
        user_id = UserId.from_string(str(uuid.uuid4()))
        soundtrack = SoundtrackBuilder().build()
        soundtrack_repository.save(soundtrack)

        users_favorite_post_request_params = {
            "user_id": user_id.value,
            "soundtrack_id": soundtrack.soundtrack_id.value
        }

        response = app.test_client().post(
            '/users/favorite',
            data=json.dumps(users_favorite_post_request_params),
            content_type='application/json'
        )

        saved_favorites: List[SoundtrackId] = user_repository.get_favorites(user_id)
        assert response.status_code == 404


  def test_should_return_404_when_adding_an_unexisting_soundtrack_to_favorites(self):
        user = UserBuilder().build()
        user_repository.save(user)
        soundtrack_id = SoundtrackId.from_string(str(uuid.uuid4()))

        users_favorite_post_request_params = {
            "user_id": user.user_id.value,
            "soundtrack_id": soundtrack_id.value
        }

        response = app.test_client().post(
            '/users/favorite',
            data=json.dumps(users_favorite_post_request_params),
            content_type='application/json'
        )

        saved_favorites: List[SoundtrackId] = user_repository.get_favorites(user.user_id)
        assert response.status_code == 404


  def test_should_return_409_when_adding_a_soundtrack_to_favorites_twice(self):
        user = UserBuilder().build()
        user_repository.save(user)
        soundtrack = SoundtrackBuilder().build()
        soundtrack_repository.save(soundtrack)
        user_repository.save_favorite(user.user_id, soundtrack.soundtrack_id)

        users_favorite_post_request_params = {
            "user_id": user.user_id.value,
            "soundtrack_id": soundtrack.soundtrack_id.value
        }

        response = app.test_client().post(
            '/users/favorite',
            data=json.dumps(users_favorite_post_request_params),
            content_type='application/json'
        )

        saved_favorites: List[SoundtrackId] = user_repository.get_favorites(user.user_id)
        assert response.status_code == 409