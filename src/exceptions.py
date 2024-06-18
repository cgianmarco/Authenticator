from constants import Messages

class InvalidCredentialsError(Exception):
    def __init__(self, message=Messages.INVALID_CREDENTIALS):
        self.message = message
        super().__init__(self.message)
        
class UserAlreadyExistsError(Exception):
    def __init__(self, message=Messages.USER_ALREADY_EXISTS):
        self.message = message
        super().__init__(self.message)
        
class RateLimitError(Exception):
    def __init__(self, message=Messages.RATE_LIMIT_EXCEEDED):
        self.message = message
        super().__init__(self.message)