from ..soundtrack_id import SoundtrackId


class UnexistingSoundtrackError(Exception):
    def __init__(self, soundtrack_id: SoundtrackId):
        self.message = "Get soundtrack by id: soundtrack with id {0} doesn't exists".format(
            soundtrack_id.value)

    def __str__(self):
        return self.message
