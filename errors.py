class InvalidQueryException(Exception):
    def __init__(self, message: str) -> None:
        self.message = message

    def __str__(self) -> str:
        return f"InvalidQueryException: {self.message}"
