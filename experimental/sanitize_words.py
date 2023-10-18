import string
import unicodedata

def sanitize_words(self, words: set[str], stop_words: set[str] = set()) -> set[str]:
    """Remove case, punctuation, stop words, and diacritics from words.

    Args:
        words (set[str]): A set of words.
        stop_words (set[str], optional): A set of stop words to remove. Defaults to an empty set.

    Returns:
        set[str]: A set of sanitized words.
    """

    def remove_diacritics(input_str):
        nfkd_form = unicodedata.normalize('NFKD', input_str)
        return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])

    sanitized_words = {
        remove_diacritics(word.lower().strip().translate(str.maketrans("", "", string.punctuation)))
        for word in words
        if word.lower() not in stop_words
    }

    return sanitized_words
