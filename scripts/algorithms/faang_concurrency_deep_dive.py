"Context: Senior Engineering Interviews (L5/L6)

Simple 'ThreadPoolExecutor' is junior level.
Seniors understand **Race Conditions**, **Deadlocks**, **Semaphores**, and **Queues**.

SCENARIOS:
1. Thread-Safe Counter (The "Race Condition" Trap)
2. Producer-Consumer (The "Backpressure" Pattern)
3. Rate Limited Crawler (Semaphore usage)
"

import threading
import queue
import time
import random
from concurrent.futures import ThreadPoolExecutor

# ==========================================
# 1. THREAD-SAFE COUNTER (Locks)
# ==========================================
class ThreadSafeCounter:
    """
    Problem: Increment a counter from multiple threads.
    Trap: 'count += 1' is NOT atomic in Python (it's read-modify-write).
    Fix: Use threading.Lock()
    """
    def __init__(self):
        self.value = 0
        self._lock = threading.Lock()

    def increment(self):
        # "Context Manager" syntax handles acquire/release automatically
        # preventing deadlocks if exceptions occur.
        with self._lock:
            self.value += 1
            # Current value is consistent only inside the lock
            val = self.value
        return val

# ==========================================
# 2. PRODUCER-CONSUMER (Queue)
# ==========================================
def producer(q, event, id):
    """Generates 'work'."""
    while not event.is_set():
        item = random.randint(1, 100)
        # put() blocks if queue is full (Backpressure!)
        try:
            q.put(item, timeout=1) 
            print(f"[P{id}] Produced {item} (Q Size: {q.qsize()})")
            time.sleep(random.uniform(0.1, 0.5))
        except queue.Full:
            continue
    print(f"[P{id}] Stopping")

def consumer(q, event, id):
    """Processes 'work'."""
    while not event.is_set() or not q.empty():
        try:
            # get() blocks if queue is empty
            item = q.get(timeout=1)
            print(f"  [C{id}] Consumed {item}")
            # Simulate work
            time.sleep(random.uniform(0.2, 0.6))
            q.task_done()
        except queue.Empty:
            continue
    print(f"  [C{id}] Stopping")

def run_producer_consumer():
    """
    Orchestrates the pipeline.
    Uses a 'Sentinel' event to signal shutdown.
    """
    work_queue = queue.Queue(maxsize=5) # Bounded Queue = Backpressure
    shutdown_event = threading.Event()
    
    threads = []
    # Start Producers
    for i in range(2):
        t = threading.Thread(target=producer, args=(work_queue, shutdown_event, i))
        t.start()
        threads.append(t)
        
    # Start Consumers
    for i in range(2):
        t = threading.Thread(target=consumer, args=(work_queue, shutdown_event, i))
        t.start()
        threads.append(t)
        
    time.sleep(3) # Let it run
    print("--- SIGNALING SHUTDOWN ---")
    shutdown_event.set()
    
    for t in threads:
        t.join()
    print("--- DONE ---")

# ==========================================
# 3. SEMAPHORE (Throttling)
# ==========================================
class ThrottledWorker:
    """
    Problem: Limit max concurrent connections to a database to 3.
    Solution: Semaphore (Token bucket).
    """
    def __init__(self, limit):
        self.sem = threading.Semaphore(limit)
        
    def access_resource(self, thread_id):
        print(f"[T{thread_id}] Waiting for token...")
        with self.sem:
            print(f"[T{thread_id}] Acquired! Working...")
            time.sleep(1) # Simulate DB query
            print(f"[T{thread_id}] Releasing.")

def run_semaphore_demo():
    worker = ThrottledWorker(limit=2) # Only 2 at a time
    with ThreadPoolExecutor(max_workers=5) as ex:
        for i in range(5):
            ex.submit(worker.access_resource, i)

# ==========================================
# MAIN
# ==========================================
if __name__ == "__main__":
    print("--- 1. LOCK DEMO (Race Condition Fix) ---")
    counter = ThreadSafeCounter()
    def worker():
        for _ in range(1000): counter.increment()
    
    threads = [threading.Thread(target=worker) for _ in range(10)]
    for t in threads: t.start()
    for t in threads: t.join()
    
    print(f"Final Count (Expected 10000): {counter.value}")
    
    print("\n--- 2. PRODUCER-CONSUMER ---")
    run_producer_consumer()
    
    print("\n--- 3. SEMAPHORE DEMO ---")
    run_semaphore_demo()
