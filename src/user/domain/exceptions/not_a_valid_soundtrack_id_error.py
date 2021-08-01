class NotAValidSoundtrackIdError(Exception):
    def __init__(self, soundtrack_id: str):
        self.message = '{0} is not a valid soundtrack_id.'.format(soundtrack_id)

    def __str__(self):
        return self.message
