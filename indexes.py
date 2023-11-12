import string
from typing import Set
from stop_words import STOP_WORDS


class Indexes:
    """Class containing methods for indexing text.

    The class contains methods for sanitizing text by removing punctuation,
    case and stop words. It also contains a method for extracting sanitized
    words from a string of text.

    Attributes
    ----------
    None

    Methods
    -------
    __sanitize_words: Removes punctuation, case and stop words from a set of words.
    get_sanitized_words: Extracts sanitized words from a string of text.

    """

    def __sanitize_words(self, words: Set[str], stop_words: Set[str] = STOP_WORDS) -> Set[str]:
        """Remove case, punctuation, and stop words from words.

        Args:
        ----
            words (list[str]): A set of words.
            stop_words (set[str], optional): A set of stop words to remove. Defaults to an empty set.

        Returns:
        -------
            set[str]: A set of sanitized words.
        """
        return {
            word.lower()
            .strip()
            .translate(str.maketrans("", "", string.punctuation))
            for word in words
            if word.lower() not in stop_words
        }

    def get_sanitized_words(self, search_text: str) -> set[str]:
        """Get sanitized words from search_text.

        Args:
        ----
            search_text (str): The text to sanitize.

        Returns:
        -------
            set[str]: A set of sanitized words.
        """
        return self.__sanitize_words(search_text.split())

    # TODO: @apinanyogaratnam: move all of the index methods to this class
