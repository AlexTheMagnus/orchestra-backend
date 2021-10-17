from typing import List

from src.soundtrack.domain.chapter.chapter import Chapter
from src.soundtrack.infrastructure.soundtrack_mysql_repository import SoundtrackMysqlRepository
from src.soundtrack.infrastructure.chapter.chapter_mysql_repository import ChapterMysqlRepository
from src.soundtrack.domain.soundtrack import Soundtrack
from src.soundtrack.application.chapter.get_soundtrack_chapters import GetSoundtrackChapters
from ...builder.soundtrack_builder import SoundtrackBuilder
from ...builder.chapter_builder import ChapterBuilder

soundtrack: Soundtrack = SoundtrackBuilder().build()
soundtrack_without_chapters: Soundtrack = SoundtrackBuilder().build()
unexisting_soundtrack: Soundtrack = SoundtrackBuilder().build()
soundtrack_repository = SoundtrackMysqlRepository()
soundtrack_repository.save(soundtrack)
soundtrack_repository.save(soundtrack_without_chapters)

chapter_repository = ChapterMysqlRepository()
use_case: GetSoundtrackChapters = GetSoundtrackChapters(chapter_repository)

for x in range(5):
    chapter: Chapter = ChapterBuilder().with_soundtrack_id(soundtrack.soundtrack_id).build()
    chapter_repository.save(chapter)

class TestGetSoundtrackChapters():
    def test_soundtrack_chapters_are_getted(self):
        found_chapters: List[Chapters] = use_case.run(soundtrack.soundtrack_id)
        assert len(found_chapters) == 5

    def test_soundtrack_without_chapters_returns_no_chapters(self):
        found_chapters: List[Soundtrack] = use_case.run(soundtrack_without_chapters.soundtrack_id)
        assert len(found_chapters) == 0

    def test_unexisting_soundtrack_returns_no_chapters(self):
        found_chapters: List[Soundtrack] = use_case.run(unexisting_soundtrack.soundtrack_id)
        assert len(found_chapters) == 0