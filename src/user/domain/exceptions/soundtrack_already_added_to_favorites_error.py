from ..user_id import UserId

class SoundtrackAlreadyAddedToFavoritesError(Exception):
    def __init__(self, str_user_id: str, str_soundtrack_id: str):
        self.message = 'User {0} have already added to favorites the soundtrack {1}'.format(
            str_user_id, str_soundtrack_id)

    def __str__(self):
        return self.message
