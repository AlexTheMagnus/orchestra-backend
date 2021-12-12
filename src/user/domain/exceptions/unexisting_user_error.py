class UnexistingUserError(Exception):
    def __init__(self, str_user_id: str):
        self.message = "User with id {0} doesn't exists".format(
            str_user_id)

    def __str__(self):
        return self.message
