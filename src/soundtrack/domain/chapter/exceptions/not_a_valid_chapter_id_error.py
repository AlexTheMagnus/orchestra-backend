class NotAValidChapterIdError(Exception):
    def __init__(self, chapter_id: str):
        self.message = '{0} is not a valid chapter_id.'.format(chapter_id)

    def __str__(self):
        return self.message
