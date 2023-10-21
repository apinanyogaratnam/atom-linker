import threading
import queue
import time

# Define the worker function
def worker(task_queue):
    while True:
        task = task_queue.get()
        if task is None:  # Sentinel value to exit thread
            break
        # Execute the task (for this example, just sleep)
        time.sleep(task)
        print(f"Completed task of {task} seconds.")
        task_queue.task_done()

# Create the task queue
tasks = queue.Queue()

# Start a fixed number of worker threads
num_threads = 5
threads = []
for _ in range(num_threads):
    t = threading.Thread(target=worker, args=(tasks,))
    t.start()
    threads.append(t)

# Add tasks to the queue (for this example, random sleep durations)
for _ in range(20):
    tasks.put(1)  # Sleep for 1 second

# Wait for all tasks to complete
tasks.join()

# Stop the worker threads
for _ in range(num_threads):
    tasks.put(None)
for t in threads:
    t.join()

print("All tasks completed!")
