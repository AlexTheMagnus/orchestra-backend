import pytest
from faker import Faker

from src.soundtrack.domain.chapter.theme import Theme
from src.soundtrack.domain.chapter.exceptions.not_a_valid_theme_url_error import NotAValidThemeUrlError

fake = Faker()


class TestTheme():

    def test_from_url_constructor(self):
        theme_url = "https://open.spotify.com/track/" + fake.pystr()
        theme = Theme.from_url(theme_url)
        assert theme.value == theme_url

    def test_building_theme_with_a_non_valid_url_throws_an_error(self):
        theme_url = fake.pystr()
        with pytest.raises(NotAValidThemeUrlError):
            theme = Theme.from_url(theme_url)
