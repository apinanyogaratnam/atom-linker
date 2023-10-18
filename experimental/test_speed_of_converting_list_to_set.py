import string
import random
import timeit
from typing import Set, List


# Functions to sanitize words
def sanitize_words_set(words: Set[str], stop_words: Set[str]) -> Set[str]:
    return {
        word.lower()
        .strip()
        .translate(str.maketrans("", "", string.punctuation))
        for word in words
        if word.lower() not in stop_words
    }


def sanitize_words_list(words: List[str], stop_words: Set[str]) -> Set[str]:
    return {
        word.lower()
        .strip()
        .translate(str.maketrans("", "", string.punctuation))
        for word in set(words)
        if word.lower() not in stop_words
    }


# Function to generate random strings
def random_string(length=5):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))


# Sample data
words_set = {random_string() for _ in range(10000000)}
words_list = list(words_set)
stop_words = {random_string() for _ in range(10000)}

# Profile the execution time of each function
time_set_large = timeit.timeit(lambda: sanitize_words_set(words_set, stop_words), number=1)
time_list_large = timeit.timeit(lambda: sanitize_words_list(words_list, stop_words), number=1)

print(f"Time for sanitize_words_set: {time_set_large} seconds")
print(f"Time for sanitize_words_list: {time_list_large} seconds")


# ➜  atom-linker git:(main) ✗ python3 experimental/test_speed_of_converting_list_to_set.py 
# Time for sanitize_words_set: 1.663094125004136 seconds
# Time for sanitize_words_list: 1.5980288749997271 seconds

# ➜  atom-linker git:(main) ✗ python3 experimental/test_speed_of_converting_list_to_set.py
# Time for sanitize_words_set: 21.738504209002713 seconds
# Time for sanitize_words_list: 26.798322291004297 seconds

# NOTE: in conclusion, no point of converting list to set and then iterating over it, just iterate over the list
