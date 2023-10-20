# NOTE: a bit more complex but reduces latency
import os
import time
import psutil
from concurrent.futures import ThreadPoolExecutor

def dynamic_max_workers(memory_per_worker=100):
    num_cores = os.cpu_count()
    available_memory = psutil.virtual_memory().available / (1024 ** 2)
    return min(num_cores, int(available_memory / memory_per_worker))

def worker_function(data):
    # ... your task logic here ...
    time.sleep(1)  # Simulate some task processing

# Initial executors
executor_active = ThreadPoolExecutor(max_workers=dynamic_max_workers())
executor_standby = ThreadPoolExecutor(max_workers=dynamic_max_workers())

try:
    while True:
        # Check memory usage
        memory_usage = 1 - psutil.virtual_memory().available / psutil.virtual_memory().total
        
        # If memory usage crosses a threshold, swap executors
        if memory_usage > 0.75:
            executor_active.shutdown(wait=True)  # Wait for the current tasks to finish
            executor_active, executor_standby = executor_standby, executor_active  # Swap roles
            # Resize the standby executor (currently the old active)
            recommended_workers = dynamic_max_workers()
            executor_standby = ThreadPoolExecutor(max_workers=recommended_workers)
        
        # Submit some tasks as an example
        for _ in range(10):
            executor_active.submit(worker_function, "some_data")
        
        time.sleep(5)  # Check memory every 5 seconds for this example

except KeyboardInterrupt:
    executor_active.shutdown(wait=True)
    executor_standby.shutdown(wait=True)
