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

# NOTE: Can't test it because it use the spotify auth and I cant mock it.
# class TestUsersPostController():
#     def test_should_grant_access_and_save_a_user_with_the_passed_parameters(self):
#         user_id: UserId = UserId.from_string(fake.pystr())
#         user_post_request_params = {'access_code': 'BsdsdsdsdPdGueqr-FYTGgAxBSM4kyjVlgnjENJ6z2rCcBX5yWbAOY3VNcYyMoY_KLEzptyZtx-zRnClNvmLgt2BBCFc9EqVYX3sENBBAcuVHjlmgTM8ASnVC62F19gvcHvb-L_zRvHg3y2MRCqZlNEYhYnNiDJSFv7JPPF4eLfXaQmiOQNoy12cc5UVJSpUiQssSA'}

#         response = app.test_client().post(
#             '/users',
#             data=json.dumps(user_post_request_params),
#             content_type='application/json'
#         )

#         found_user = user_repository.find(user_id)
#         assert response.status_code == 200
#         data = json.loads(response.get_data(as_text=True))
#         assert data["access_token"] != None
#         assert data["user_id"] != None
#         assert data["username"] != None
#         assert data["user_avatar"] != None

class TestUsersGetController():
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