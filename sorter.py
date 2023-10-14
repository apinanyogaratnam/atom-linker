import logging
import multiprocessing
import os
from multiprocessing.pool import ThreadPool

file_name = os.path.basename(__file__)
logger = logging.getLogger(file_name)

# Setup logger to write to file
fh = logging.FileHandler(f"{file_name}.log")
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)

# Ensure logger is set to debug level, so it logs messages of DEBUG and above.
logger.setLevel(logging.DEBUG)


class Sorter:
    @staticmethod
    def merge_sort(arr: list[object], sort_by: str) -> list[object]:
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
        logger.debug(f"Records: {records}")  # Debug line

        # Ensure records is a list and non-empty
        assert isinstance(records, list), f"Expected a list, but got {type(records)}"
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

