import pytest
import pyisbn
from .exceptions.not_a_valid_isbn_13_error import NotAValidIsbn13Error


class Isbn13():

    def __init__(self, isbn_13: str):
        self.__validate_isbn_13_format(isbn_13)
        self.__value: str = isbn_13

    @staticmethod
    def from_string(isbn_13: str):
        return Isbn13(isbn_13)

    @property
    def value(self):
        return self.__value

    def __validate_isbn_13_format(self, str_isbn_13: str):
        if not pyisbn.validate(str_isbn_13):
            raise(NotAValidIsbn13Error(str_isbn_13))
