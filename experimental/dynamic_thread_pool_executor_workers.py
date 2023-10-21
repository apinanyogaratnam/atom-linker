# NOTE: a bit more latency but less complex
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

# Initial executor
executor = ThreadPoolExecutor(max_workers=dynamic_max_workers())

try:
    while True:
        # Submit some tasks as an example
        for _ in range(10):
            executor.submit(worker_function, "some_data")
        
        # Sleep and periodically check memory to adjust max_workers
        time.sleep(5)  # Check every 5 seconds for this example
        
        current_workers = executor._max_workers
        recommended_workers = dynamic_max_workers()
        
        if current_workers != recommended_workers:
            # Wait for the current tasks to finish
            executor.shutdown(wait=True)
            # Create a new executor with the updated max_workers value
            executor = ThreadPoolExecutor(max_workers=recommended_workers)
            print(f"Adjusted max_workers from {current_workers} to {recommended_workers}")

except KeyboardInterrupt:
    executor.shutdown(wait=True)
