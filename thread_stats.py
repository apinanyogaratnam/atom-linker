from collections import defaultdict
from stats import Stats
from stats_enums import StatsType


class ThreadStats(Stats):
    def __init__(self) -> None:
        self.name = StatsType.THREADS

        super().__init__()

    def average_threads_per_minute(self) -> float:
        data = self.get(self.name)
        if not data:
            return 0

        store = defaultdict(int)

        for entry in data:
            timestamp = entry['timestamp'].strftime('%Y-%m-%d %H:%M')
            store[timestamp] += 1

        return sum(store.values()) / len(store) if store else 0
