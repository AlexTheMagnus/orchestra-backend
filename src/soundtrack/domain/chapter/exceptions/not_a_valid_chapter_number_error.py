class NotAValidChapterNumberError(Exception):
    def __init__(self, chapter_number: int):
        self.message = '{0} is not a valid chapter_number.'.format(
            chapter_number)

    def __str__(self):
        return self.message
