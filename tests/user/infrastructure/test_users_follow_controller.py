from faker import Faker
from typing import List
import json

from ..builder.user_builder import UserBuilder
from orchestra import app
from src.user.domain.user import User
from src.user.infrastructure.from_user_to_dict import FromUserToDict
from src.user.infrastructure.user_mysql_repository import UserMysqlRepository

fake = Faker()
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


class TestUsersFollowGetController():

    def test_should_return_the_followers(self):
        user = UserBuilder().build()
        user_repository.save(user)
        follower_list: List[User] = []

        for x in range(fake.random_number(1)):
            follower: User = UserBuilder().build()
            user_repository.save(follower)
            user_repository.save_follow(follower.user_id, user.user_id)
            follower_list.append(follower)

        response = app.test_client().get(
            '/users/{0}/followers'.format(user.user_id.value),
            content_type='application/json'
        )

        assert response.status_code == 200
        data = json.loads(response.get_data(as_text=True))
        assert len(data["followers"]) == len(follower_list)

        dict_follower_list = FromUserToDict.with_user_list(follower_list)
        for follower in data["followers"]:
            assert follower in dict_follower_list


    def test_should_return_the_followed_users(self):
        user = UserBuilder().build()
        user_repository.save(user)
        followed_user_list: List[User] = []

        for x in range(fake.random_number(1)):
            followed_user: User = UserBuilder().build()
            user_repository.save(followed_user)
            user_repository.save_follow(user.user_id, followed_user.user_id)
            followed_user_list.append(followed_user)

        response = app.test_client().get(
            '/users/{0}/followed-users'.format(user.user_id.value),
            content_type='application/json'
        )

        assert response.status_code == 200
        data = json.loads(response.get_data(as_text=True))
        assert len(data["followed_users"]) == len(followed_user_list)

        dict_followed_user_list = FromUserToDict.with_user_list(followed_user_list)
        for follower in data["followed_users"]:
            assert follower in dict_followed_user_list


class TestUsersFollowDeleteController():
    def test_should_unfollow_a_user(self):
        follower: User = UserBuilder().build()
        user_repository.save(follower)
        followed_user: User = UserBuilder().build()
        user_repository.save(followed_user)
        user_repository.save_follow(follower.user_id, followed_user.user_id)

        response = app.test_client().delete(
            '/users/{0}/unfollow/{1}'.format(follower.user_id.value, followed_user.user_id.value),
            content_type='application/json'
        )

        assert response.status_code == 204

        found_follows: List[SoundtrackId] = user_repository.get_followed_users(follower.user_id)
        assert found_follows == []


    def test_should_return_404_when_unfollowing_a_non_followed_user(self):
        follower: User = UserBuilder().build()
        user_repository.save(follower)
        followed_user: User = UserBuilder().build()
        user_repository.save(followed_user)

        response = app.test_client().delete(
            '/users/{0}/unfollow/{1}'.format(follower.user_id.value, followed_user.user_id.value),
            content_type='application/json'
        )

        assert response.status_code == 404