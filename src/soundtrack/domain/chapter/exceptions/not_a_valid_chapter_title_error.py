class NotAValidChapterTitleError(Exception):
    def __init__(self, chapter_title: str):
        self.message = '{0} is not a valid chapter title.'.format(
            chapter_title)

    def __str__(self):
        return self.message
