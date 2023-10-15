import multiprocessing
from multiprocessing.pool import ThreadPool

from log import get_logger

logger = get_logger(__file__)


class Sorter:
    """Class for sorting lists of objects.

    Provides methods for parallel merge sort and merging sorted lists.
    Designed to take advantage of multiple cores by splitting
    the data into chunks and sorting in parallel threads.

    Attributes
    ----------
    None

    Methods
    -------
    merge_sort: Recursively split list and merge sort each half.
    merge: Merge two already sorted lists into one sorted list.
    parallel_sorting: Main method to sort a list in parallel.
    """

    @staticmethod
    def merge_sort(arr: list[object], sort_by: str) -> list[object]:
        """Recursively split list and merge sort each half.

        Splits the input list in half, recursively sorts each half, and merges
        the sorted halves back together. Base case returns list if length <= 1.

        Args:
        ----
        arr (list[object]): List to sort.
        sort_by (str): Key in each object to sort by.

        Returns:
        -------
        list[object]: Sorted version of input list.
        """
        if len(arr) <= 1:
            return arr

        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]

        left_half = Sorter.merge_sort(left_half, sort_by)
        right_half = Sorter.merge_sort(right_half, sort_by)

        return Sorter.merge(left_half, right_half, sort_by)

    @staticmethod
    def merge(left: list[object], right: list[object], sort_by: str) -> list[object]:
        """Merge two sorted lists into one sorted list.

        Iterates through both lists simultaneously, comparing elements at each
        index. Pushes the smaller element to the result list each iteration.

        Args:
        ----
        left (list[object]): First sorted list.
        right (list[object]): Second sorted list.
        sort_by (str): Key in each object to compare for sorting.

        Returns:
        -------
        list[object]: Combined sorted list.
        """
        result = []
        left_idx, right_idx = 0, 0

        while left_idx < len(left) and right_idx < len(right):
            left_elem = left[left_idx].get(sort_by)
            right_elem = right[right_idx].get(sort_by)

            if left_elem < right_elem:
                result.append(left[left_idx])
                left_idx += 1
            else:
                result.append(right[right_idx])
                right_idx += 1

        result += left[left_idx:]
        result += right[right_idx:]
        return result

    def parallel_sorting(self, records: list[object], sort_by: str = "created_at") -> list[object]:
        """Sort a list using merge sort in parallel.

        Splits the list into chunks and uses thread pool to sort
        each chunk in parallel. Then merges the sorted chunks.

        Args:
        ----
        records (list[object]): List of records to sort.
        sort_by (str): Key in each record to sort by.

        Returns:
        -------
        list[object]: Sorted records.

        """
        logger.debug(f"Records: {records}")  # Debug line

        if not records:
            return []

        cpu_count = multiprocessing.cpu_count()
        avg_len = len(records) // cpu_count
        chunks = [records[i * avg_len: (i + 1) * avg_len] for i in range(cpu_count - 1)]
        chunks.append(records[(cpu_count - 1) * avg_len:])

        logger.debug(f"Chunks: {chunks}")  # Debug line

        with ThreadPool(cpu_count) as pool:
            sorted_chunks = pool.starmap(self.merge_sort, [(chunk, sort_by) for chunk in chunks])

        logger.debug(f"Sorted Chunks: {sorted_chunks}")  # Debug line

        while len(sorted_chunks) > 1:
            merged_chunks = []
            for i in range(0, len(sorted_chunks), 2):
                if i + 1 < len(sorted_chunks):
                    merged = self.merge(sorted_chunks[i], sorted_chunks[i + 1], sort_by)
                    merged_chunks.append(merged)
                else:
                    merged_chunks.append(sorted_chunks[i])

            logger.debug(f"Merging: {sorted_chunks} => {merged_chunks}")  # Debug line
            sorted_chunks = merged_chunks

        return sorted_chunks[0] if sorted_chunks else []

