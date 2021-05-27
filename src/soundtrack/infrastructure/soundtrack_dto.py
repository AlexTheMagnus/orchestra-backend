from typing import TypedDict


class ChapterDTO(TypedDict):
    chapter_id: str
    chapter_number: int
    theme: str
    chapter_title: str


class SoundtrackDTO(TypedDict):
    user_id: str
    book: str
    author: str
    chapters: list[ChapterDTO]
