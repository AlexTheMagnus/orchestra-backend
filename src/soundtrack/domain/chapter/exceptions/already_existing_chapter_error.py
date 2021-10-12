class AlreadyExistingChapterError(Exception):
    def __init__(self, chapter_id: str):
        self.message = 'Add chapter: Chapter with id {0} already exists'.format(
            chapter_id)

    def __str__(self):
        return self.message
