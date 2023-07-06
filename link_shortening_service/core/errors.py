class BaseError(Exception):
    message: str

    def __init__(self, message: str):
        self.message = message
        super().__init__()
