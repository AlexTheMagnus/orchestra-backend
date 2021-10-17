from typing import List

from ...domain.chapter.chapter import Chapter


class FromChapterToDict:

    def __init__(self):
        pass

    @staticmethod
    def with_chapter(chapter: Chapter):    
        chapter_dict = {
            "chapter_id": chapter.chapter_id.value,
            "soundtrack_id": chapter.soundtrack_id.value,
            "chapter_number": chapter.chapter_number.value,
            "theme": chapter.theme.value,
            "chapter_title": chapter.chapter_title.value
        }

        return chapter_dict

    @staticmethod
    def with_chapters_list(chapters_list: List[Chapter]):
        chapters_list_dict = { "chapters_list": [] }
        
        for chapter in chapters_list:
            chapter_dict = FromChapterToDict.with_chapter(chapter)
            chapters_list_dict["chapters_list"].append(chapter_dict)

        return chapters_list_dict