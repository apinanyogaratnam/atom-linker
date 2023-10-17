from datetime import datetime, timezone
from time import perf_counter

from log import get_logger
from experimental.sorter import Sorter

logger = get_logger(__file__)

lst = [{
    "created_at": datetime.now(tz=timezone.utc),
}]
lst *= 10000000

start_time = perf_counter()

s = Sorter()
items = s.parallel_sorting(lst, "created_at")

end_time = perf_counter()

logger.debug(f"Time elapsed: {end_time - start_time}")

start_time = perf_counter()
items = sorted(lst, key=lambda x: x["created_at"])
end_time = perf_counter()

logger.debug(f"Time elapsed: {end_time - start_time}")
