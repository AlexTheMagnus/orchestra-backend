import pyisbn


class Isbn13():

    def __init__(self, isbn_13: str):
        self.__validate_uuid_v4_format(isbn_13)
        self.__value: str = isbn_13

    @staticmethod
    def from_string(isbn_13: str):
        return Isbn13(isbn_13)

    @property
    def value(self):
        return self.__value

    def __validate_uuid_v4_format(self, str_isbn_13: str):
        if not pyisbn.validate(str_isbn_13):
            raise(NotAValidIsbn13Error(uuid_soundtrack_id))
