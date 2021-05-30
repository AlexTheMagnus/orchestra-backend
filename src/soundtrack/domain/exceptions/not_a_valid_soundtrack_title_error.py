class NotAValidSoundtrackTitleError(Exception):
    def __init__(self, soundtrack_title: str):
        self.message = '{0} is not a valid soundtrack title.'.format(
            soundtrack_title)

    def __str__(self):
        return self.message
