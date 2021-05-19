import pytest
from faker import faker

fake = Faker()


class TestNumber():

    def test_from_integer_constructor(self):
        int_chapter_number = fake.random_number(2)
        chapter_id = Number.from_string(int_chapter_number)
        assert chapter_id.value == int_chapter_number

    def test_building_chapter_id_with_a_non_uuid4_throws_an_error(self):
        int_chapter_number = str(uuid.uuid1())
        with pytest.raises(NotAValidNumberError):
            chapter_id = Number.from_string(int_chapter_number)
