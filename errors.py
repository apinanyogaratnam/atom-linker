class InvalidQueryError(Exception):
    """Exception class for representing an invalid query error.

    This exception is raised when an invalid query is encountered. It stores the error message for the invalid query.

    Args:
    ----
    message: The error message.

    Returns:
    -------
    None
    """

    def __init__(self, message: str) -> None:
        """Initialize the object.

        Sets the error message for the object.

        Args:
        ----
        self: The instance of the class.
        message: The error message.

        Returns:
        -------
        None
        """
        self.message = message

    def __str__(self) -> str:
        """Return a string representation of the object.

        Returns a string representation of the InvalidQueryError object, including the error message.

        Args:
        ----
        self: The instance of the class.

        Returns:
        -------
        str: The string representation of the object.
        """
        return f"InvalidQueryError: {self.message}"
