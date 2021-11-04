class AlreadyLikedSoundtrackError(Exception):
    def __init__(self, user_id: str, soundtrack_id: str):
        self.message = 'Like soundtrack: User {0} have alredy liked the soundtrack {1}'.format(
            user_id, soundtrack_id)

    def __str__(self):
        return self.message
