import pytest

from src.soundtrack.domain.isbn_13 import Isbn13
from src.soundtrack.domain.not_a_valid_isbn_13_error import NotAValidIsbn13Error


class TestIsbn13():

    def test_from_string_constructor(self):
        str_valid_isbn_13 = "978-2-1550-9533-9"
        isbn_13 = Isbn13.from_string(str_valid_isbn_13)
        assert isbn_13.value == str_valid_isbn_13

    def test_building_isbn_13_with_a_non_valid_isbn_13_throws_an_error(self):
        str_non_valid_isbn_13 = "978-2-1550-9533-1"
        with pytest.raises(NotAValidIsbn13Error):
            isbn_13 = Isbn13.from_string(str_non_valid_isbn_13)
