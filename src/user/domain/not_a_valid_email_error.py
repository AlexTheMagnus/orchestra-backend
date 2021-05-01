class NotAValidEmailError(Exception):
    def __init__(self, str_email: str):
        self.message = 'Email: {0} is not a valid email.'.format(
            str_email)

    def __str__(self):
        return self.message
