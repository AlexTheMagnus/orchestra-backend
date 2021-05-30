class NotAValidIsbn13Error(Exception):
    def __init__(self, isbn_13: str):
        self.message = '{0} is not a valid isbn 13.'.format(isbn_13)

    def __str__(self):
        return self.message
