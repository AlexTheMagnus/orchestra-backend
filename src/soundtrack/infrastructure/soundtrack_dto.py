from typing import TypedDict

from src.soundtrack.infrastructure.chapter.chapter_dto import ChapterDTO


class SoundtrackDTO(TypedDict):
    user_id: str
    book: str
    author: str
    chapters: list[ChapterDTO]
