from typing import List
import json

from ..builder.user_builder import UserBuilder
from orchestra import app
from src.user.domain.user import User
from src.user.infrastructure.user_mysql_repository import UserMysqlRepository

user_repository = UserMysqlRepository()

def teardown_module():
    user_repository.clean()

class TestUsersFollowPostController():
    
    def test_should_follow_a_user(self):
        follower_user = UserBuilder().build()
        user_repository.save(follower_user)
        followed_user = UserBuilder().build()
        user_repository.save(followed_user)

        users_follow_post_request_params = {
            "follower_id": follower_user.user_id.value,
            "followed_id": followed_user.user_id.value
        }

        response = app.test_client().post(
            '/users/follow',
            data=json.dumps(users_follow_post_request_params),
            content_type='application/json'
        )

        saved_followers: List[User] = user_repository.get_followers(followed_user.user_id)
        assert response.status_code == 200
        assert len(saved_followers) == 1
        assert saved_followers[0].user_id.value == follower_user.user_id.value
        assert saved_followers[0].username.value == follower_user.username.value
        assert saved_followers[0].user_avatar.value == follower_user.user_avatar.value


    def test_should_return_404_when_an_unexisting_user_follows_a_user(self):
        follower_user = UserBuilder().build()
        followed_user = UserBuilder().build()
        user_repository.save(followed_user)

        users_follow_post_request_params = {
            "follower_id": follower_user.user_id.value,
            "followed_id": followed_user.user_id.value
        }

        response = app.test_client().post(
            '/users/follow',
            data=json.dumps(users_follow_post_request_params),
            content_type='application/json'
        )

        assert response.status_code == 404


    def test_should_return_404_when_following_an_unexisting_user(self):
        follower_user = UserBuilder().build()
        user_repository.save(follower_user)
        followed_user = UserBuilder().build()

        users_follow_post_request_params = {
            "follower_id": follower_user.user_id.value,
            "followed_id": followed_user.user_id.value
        }

        response = app.test_client().post(
            '/users/follow',
            data=json.dumps(users_follow_post_request_params),
            content_type='application/json'
        )

        assert response.status_code == 404
        

    def test_should_return_409_follow_twice_a_user(self):
        follower_user = UserBuilder().build()
        user_repository.save(follower_user)
        followed_user = UserBuilder().build()
        user_repository.save(followed_user)
        user_repository.save_follow(follower_user.user_id, followed_user.user_id)

        users_follow_post_request_params = {
            "follower_id": follower_user.user_id.value,
            "followed_id": followed_user.user_id.value
        }

        response = app.test_client().post(
            '/users/follow',
            data=json.dumps(users_follow_post_request_params),
            content_type='application/json'
        )

        assert response.status_code == 409