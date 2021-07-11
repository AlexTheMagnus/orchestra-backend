from typing import TypedDict, List

from ..infrastructure.chapter.chapter_dto import ChapterDTO


class SoundtrackDTO(TypedDict):
    soundtrack_id: str
    book: str
    soundtrack_title: str
    author: str
    chapters: List[ChapterDTO]
