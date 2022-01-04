class UnexistingChapterError(Exception):
    def __init__(self, str_chapter_id: str):
        self.message = "Chapter with id {0} doesn't exists".format(
            str_chapter_id)

    def __str__(self):
        return self.message
