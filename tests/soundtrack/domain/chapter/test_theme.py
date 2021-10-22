import pytest
from faker import Faker

from src.soundtrack.domain.chapter.theme import Theme

fake = Faker()

class TestTheme():

    def test_from_string_constructor(self):
        theme_str = fake.pystr()
        theme = Theme.from_string(theme_str)
        assert theme.value == theme_str

