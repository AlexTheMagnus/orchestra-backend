from faker import Faker

from ...builder.chapter_builder import ChapterBuilder
from ...builder.soundtrack_builder import SoundtrackBuilder
from ...infrastructure.chapter.chapter_in_memory_repository import ChapterInMemoryRepository
from ...infrastructure.soundtrack_in_memory_repository import SoundtrackInMemoryRepository
from src.soundtrack.application.chapter.update_chapter import UpdateChapter
from src.soundtrack.domain.chapter.chapter_number import ChapterNumber
from src.soundtrack.domain.chapter.chapter_title import ChapterTitle
from src.soundtrack.domain.chapter.theme import Theme

fake = Faker()

chapter_repository = ChapterInMemoryRepository()
soundtrack_repository = SoundtrackInMemoryRepository()
use_case = UpdateChapter(chapter_repository)


class TestUpdateChapter():
    def test_chapter_number_is_updated(self):
        soundtrack = SoundtrackBuilder().build()
        soundtrack_repository.save(soundtrack)
        chapter = ChapterBuilder().with_soundtrack_id(soundtrack.soundtrack_id).build()
        chapter_repository.save(chapter)

        new_chapter_number = ChapterNumber.from_integer(fake.random_number(2))
        use_case.run(chapter.chapter_id, {
            'chapter_number': new_chapter_number,
            'theme': None,
            'chapter_title': None
        })

        found_chapter = chapter_repository.find(chapter.chapter_id)
        assert found_chapter != None
        assert found_chapter.chapter_id.value == chapter.chapter_id.value
        assert found_chapter.soundtrack_id.value == chapter.soundtrack_id.value
        assert found_chapter.chapter_number.value == new_chapter_number.value
        assert found_chapter.theme.value == chapter.theme.value
        assert found_chapter.chapter_title.value == chapter.chapter_title.value


    def test_chapter_theme_is_updated(self):
        soundtrack = SoundtrackBuilder().build()
        soundtrack_repository.save(soundtrack)
        chapter = ChapterBuilder().with_soundtrack_id(soundtrack.soundtrack_id).build()
        chapter_repository.save(chapter)

        new_theme = Theme.from_string(fake.pystr())
        use_case.run(chapter.chapter_id, {
            'chapter_number': None,
            'theme': new_theme,
            'chapter_title': None
        })

        found_chapter = chapter_repository.find(chapter.chapter_id)
        assert found_chapter != None
        assert found_chapter.chapter_id.value == chapter.chapter_id.value
        assert found_chapter.soundtrack_id.value == chapter.soundtrack_id.value
        assert found_chapter.chapter_number.value == chapter.chapter_number.value
        assert found_chapter.theme.value == new_theme.value
        assert found_chapter.chapter_title.value == chapter.chapter_title.value


    def test_chapter_title_is_updated(self):
        soundtrack = SoundtrackBuilder().build()
        soundtrack_repository.save(soundtrack)
        chapter = ChapterBuilder().with_soundtrack_id(soundtrack.soundtrack_id).build()
        chapter_repository.save(chapter)

        new_chapter_title = ChapterTitle.from_string(fake.pystr())
        use_case.run(chapter.chapter_id, {
            'chapter_number': None,
            'theme': None,
            'chapter_title': new_chapter_title
        })

        found_chapter = chapter_repository.find(chapter.chapter_id)
        assert found_chapter != None
        assert found_chapter.chapter_id.value == chapter.chapter_id.value
        assert found_chapter.soundtrack_id.value == chapter.soundtrack_id.value
        assert found_chapter.chapter_number.value == chapter.chapter_number.value
        assert found_chapter.theme.value == chapter.theme.value
        assert found_chapter.chapter_title.value == new_chapter_title.value
