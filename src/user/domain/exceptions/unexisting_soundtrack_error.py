class UnexistingSoundtrackError(Exception):
    def __init__(self, str_soundtrack_id: str):
        self.message = "Get soundtrack by id: soundtrack with id {0} doesn't exists".format(
            str_soundtrack_id)

    def __str__(self):
        return self.message
