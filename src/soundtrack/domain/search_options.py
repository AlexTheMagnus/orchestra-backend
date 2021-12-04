from typing import TypedDict
from .isbn_13 import Isbn13

class SearchOptions(TypedDict):
    book: Isbn13