import threading
import time
from typing import Any, List, TypeVar, Generic
from collections import deque

# ------------- Sentinel: unique object that cannot collide with real data  -------------
SENTINEL = object()
T = TypeVar("T")

# ------------- Blocking Queue Implementation -------------
class BlockingQueue(Generic[T]):
    """
        INTERVIEW NOTE: 
        In a real production environment, I would use python's built-in `queue.Queue`.
        I am manually implementing this here to demonstrate understanding of 
        Wait/Notify mechanisms & condition variables as requested.
    """
    def __init__(self, max_size: int = 10):
        if max_size <= 0:
            raise ValueError("max_size must be greater than 0.")

        self.max_size = max_size
        self.queue: deque[T] = deque()
        self.lock = threading.Lock()
        self.not_empty = threading.Condition(self.lock)
        self.not_full = threading.Condition(self.lock)

    def put(self, item: T) -> None:
        """Put an item into the queue, blocking if full."""
        with self.not_full:
            while len(self.queue) >= self.max_size:
                self.not_full.wait()

            self.queue.append(item)

            # Wake exactly ONE waiting consumer
            self.not_empty.notify()

    def get(self) -> T:
        """Remove and return an item from the queue, blocking if empty."""
        with self.not_empty:
            while len(self.queue) == 0:
                self.not_empty.wait()

            item = self.queue.popleft()  # O(1)

            # Wake ONE waiting producer
            self.not_full.notify()

            return item

    def size(self) -> int:
        """Return current queue length."""
        with self.lock:
            return len(self.queue)


# ------------- Producer Implementation -------------
class Producer(threading.Thread):
    """
    Producer thread: Reads from a source and places items into the blocking queue.
    """

    def __init__(self, source: List[T], queue: BlockingQueue[T], sentinel: Any):
        super().__init__()
        self.source = source
        self.queue = queue
        self.sentinel = sentinel

    def run(self):
        """ try/finally for sending sentinel even on failure. """
        try:
            for item in self.source:
                self.queue.put(item)
                print(f"[Producer] Produced: {item} | Queue size: {self.queue.size()}")
        except Exception as e:
            print(f"[Producer] ERROR: {e!r}")
        finally:
            # Always send shutdown signal
            self.queue.put(self.sentinel)
            print("[Producer] Sentinel sent.")


# ------------- Consumer Implementation -------------
class Consumer(threading.Thread):
    """
    Consumer thread: Retrieves items from queue and stores them in destination list.
    """

    def __init__(self, queue: BlockingQueue[T], destination: List[T], sentinel: Any):
        super().__init__()
        self.queue = queue
        self.destination = destination
        self.sentinel = sentinel

    def run(self):
        while True:
            item = self.queue.get()

            # Sentinel → graceful shutdown
            if item is self.sentinel:
                print("[Consumer] Received sentinel. Exiting.")
                break

            self.destination.append(item)
            print(f"[Consumer] Consumed: {item} | Queue size: {self.queue.size()}")


def run_pipeline(source: List[T], queue_size: int = 10) -> List[T]:
    """
    Producer-consumer pipeline for Assignment 1.
    
    Testing Objectives: 
    1. Thread synchronization
    2. Concurrent programming
    3. Blocking queues
    4. Wait/Notify mechanism
    """

    queue: BlockingQueue[T] = BlockingQueue(max_size=queue_size)
    destination: List[T] = []

    producer = Producer(source, queue, SENTINEL)
    consumer = Consumer(queue, destination, SENTINEL)

    start = time.time()
    producer.start()
    consumer.start()

    producer.join()
    consumer.join()
    end = time.time()

    print("\n=== Pipeline Summary ===")
    print(f"Produced:  {len(source)} items")
    print(f"Consumed:  {len(destination)} items")
    print(f"Time:      {end - start:.4f}s")

    return destination


if __name__ == "__main__":
    source_data = [1, 2, None, 4]
    output = run_pipeline(source_data, queue_size=5)
    print("\nFinal Output:", output)
