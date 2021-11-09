class UnexistingLikeError(Exception):
    def __init__(self, str_user_id: str, str_soundtrack_id: str):
        self.message = "User {0} hasn't liked the soundtrack {1}".format(
            str_user_id, str_soundtrack_id)

    def __str__(self):
        return self.message
