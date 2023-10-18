import string

from stop_words import STOP_WORDS


class Indexes:
    def __sanitize_words(self, words: set[str], stop_words: list[str] = STOP_WORDS) -> set[str]:
        """Remove case, punctuation, and stop words from words.

        Args:
            words (list[str]): A set of words.
            stop_words (set[str], optional): A set of stop words to remove. Defaults to an empty set.

        Returns:
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
            search_text (str): The text to sanitize.

        Returns:
            set[str]: A set of sanitized words.
        """

        return self.__sanitize_words(search_text.split())

    # TODO: @apinanyogaratnam: move all of the index methods to this class