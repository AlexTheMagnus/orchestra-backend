class AlreadyExistingSoundtrackError(Exception):
    def __init__(self, soundtrack_id: str):
        self.message = 'Create soundtrack: Soundtrack with id {0} already exists'.format(
            soundtrack_id)

    def __str__(self):
        return self.message
