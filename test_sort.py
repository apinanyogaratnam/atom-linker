import logging
import os
from datetime import datetime, timezone
from time import perf_counter

from sorter import Sorter

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
