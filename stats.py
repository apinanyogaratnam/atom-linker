from collections import defaultdict
from datetime import datetime

import pytz


class Stats:
    def __init__(self) -> None:
        self._stats = defaultdict(list)

    def insert(self, name: str, value: float) -> None:
        if name not in self._stats:
            self._stats[name] = []

        self._stats[name].append({
            "value": value,
            "timestamp": datetime.now(pytz.utc),
        })

    def get(self, name: str) -> list:
        return self._stats[name]
