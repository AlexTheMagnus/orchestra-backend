class UnexistingFollowError(Exception):
    def __init__(self, str_follower_id: str, str_followed_user_id: str):
        self.message = "User {0} isn't following user {1}".format(
          str_follower_id, str_followed_user_id)

    def __str__(self):
        return self.message
