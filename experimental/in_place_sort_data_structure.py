import bisect


class SortedList:
    def __init__(self):
        self._list = []

    def insert(self, value):
        bisect.insort(self._list, value)

    def __str__(self):
        return str(self._list)


sl = SortedList()
sl.insert(5)
sl.insert(3)
sl.insert(8)
print(sl)  # Output: [3, 5, 8]
