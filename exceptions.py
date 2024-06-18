class InvalidCredentialsError(Exception):
    def __init__(self, message="Invalid credentials."):
        self.message = message
        super().__init__(self.message)
        
class UserAlreadyExistsError(Exception):
    def __init__(self, message="User already exists."):
        self.message = message
        super().__init__(self.message)
        
class RateLimitError(Exception):
    def __init__(self, message="Rate limit exceeded."):
        self.message = message
        super().__init__(self.message)