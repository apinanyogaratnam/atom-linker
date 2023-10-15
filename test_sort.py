from sorter import Sorter
from datetime import datetime

from time import perf_counter

lst = [{
    'created_at': datetime.now(),
}]
lst *= 10000000

start_time = perf_counter()

s = Sorter()
items = s.parallel_sorting(lst, 'created_at')

end_time = perf_counter()

print(f"Time elapsed: {end_time - start_time}")

start_time = perf_counter()
items = sorted(lst, key=lambda x: x['created_at'])
end_time = perf_counter()

print(f"Time elapsed: {end_time - start_time}")
