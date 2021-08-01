import pytest
import json
from faker import Faker

from orchestra import app
from src.user.infrastructure.user_mysql_repository import UserMysqlRepository
from src.user.domain.user_id import UserId
from ..builder.user_builder import UserBuilder

fake = Faker()
user_repository = UserMysqlRepository()

def teardown_module():
    UserMysqlRepository().clean()

class TestUsersPostController():
    def test_should_create_and_save_a_user_with_the_passed_parameters(self):
        user_id: UserId = UserId.from_string(fake.pystr())
        user_post_request_params = get_user_post_request_params_with_id(user_id)

        response = app.test_client().post(
            '/users',
            data=json.dumps(user_post_request_params),
            content_type='application/json'
        )

        found_user = user_repository.find(user_id)
        assert response.status_code == 200
        assert found_user != None
        assert found_user.user_id.value == user_post_request_params["user_id"]
        assert found_user.username.value == user_post_request_params["username"]
        assert found_user.user_avatar.value == user_post_request_params["user_avatar"]

def get_user_post_request_params_with_id(user_id: UserId):
    return {
        "user_id": user_id.value,
        "username": fake.name(),
        "user_avatar": "https://" + fake.pystr()
    }

class TestUserGetController():
    def test_should_return_the_user_info(self):
        user: User = UserBuilder().build()
        user_repository.save(user)

        response = app.test_client().get(
            '/users/{0}'.format(user.user_id.value),
            content_type='application/json'
        )

        assert response.status_code == 200
        data = json.loads(response.get_data(as_text=True))
        assert data["user_id"] == user.user_id.value
        assert data["username"] == user.username.value
        assert data["user_avatar"] == user.user_avatar.value