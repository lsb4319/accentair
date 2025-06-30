import concurrent.futures
import threading
import time

# Function to perform a task
def perform_task(task):
    time.sleep(1)
    # Perform the task here
    print(f"Task {task} is executed by thread {threading.current_thread().name}")

# Number of tasks
num_tasks = 100

# Create a thread pool with a maximum of 5 threads
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    # Submit tasks to the thread pool
    for task in range(num_tasks):
        executor.submit(perform_task, task)
