class UnexistingFavoriteError(Exception):
    def __init__(self, str_user_id: str, str_soundtrack_id: str):
        self.message = "Soundtrack {0} isn't in the user {1}'s favorites".format(
          str_soundtrack_id, str_user_id)

    def __str__(self):
        return self.message
