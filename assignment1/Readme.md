# Intuit Build Challenge: Producer-Consumer Synchronization

[![Language](https://img.shields.io/badge/Python-3.9%2B-blue.svg?style=flat&logo=python)](https://www.python.org/)

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)]()

[![Pattern](https://img.shields.io/badge/Pattern-Producer%20Consumer-orange.svg)]()

[![Assignment](https://img.shields.io/badge/Assignment-1-blueviolet.svg)]()

> **Assignment 1:** Implement a producer-consumer pattern with thread synchronization, blocking queues, and a robust wait/notify mechanism.

---

## 📖 Overview

This project implements a thread-safe **Producer-Consumer pipeline** without relying on Python's high-level `queue.Queue`. Instead, it demonstrates a deep understanding of concurrency by manually implementing a **Monitor Object pattern** using `threading.Condition`, `threading.Lock`, and `wait()`/`notify()` semantics.

The system simulates concurrent data transfer where a Producer thread reads from a source and safely pushes to a bounded buffer, while a Consumer thread retrieves and processes data, ensuring zero race conditions or deadlocks.

### Project Structure

```bash
assignment1/
│
├── producer_consumer.py     # Main implementation
├── test_producer_consumer.py # Unit tests
└── README.md                # This file
```

## 🧠 Design Overview

### 1. BlockingQueue<T> (Custom Bounded Blocking Queue)
A manually implemented, generic, FIFO queue that supports safe concurrent access.

- **Purpose:** To demonstrate understanding of:
    - `threading.Lock`
    - `threading.Condition`
    - Blocking semantics (`wait`/`notify`)
    - Bounded queue behavior as required by the Intuit Build Challenge.

- **Key Behaviors:** 
    - Bounded size — capacity fixed at initialization.
    - put(item)
        - Blocks when queue is full
        - Wakes one waiting consumer after enqueue
    - get(item)
        - Blocks when queue is empty
        - Wakes one waiting producer after dequeue
    - Thread-safe for multiple producers and consumers

- **Internal Implementation:**
    - Stores items in a `deque` (O(1) append/popleft).
    - Uses one shared lock (`threading.Lock`) and two condition variables on that same lock:
        - `not_full` → used by producers when the queue is full.
        - `not_empty` → used by consumers when the queue is empty.
    - Both `put()` and `get()` methods:
        - Wait using `Condition.wait()` inside a `while` loop (correct pattern to avoid spurious wake-ups).
        - Call `Condition.notify()` after modifying queue state.

**Why not use `queue.Queue`?**
    Python already provides a thread-safe bounded queue. However, this challenge explicitly requires demonstrating `condition variables` and **manual synchronization**, so a custom implementation is used.

### 2. Producer Thread

- **Responsibility:**
    - Reads items from a source list and inserts them into the blocking queue.

- **Key Features:**
    - Iterates through the provided source list.
    - Calls `queue.put(item)` for each element.
    - Logs each produced value.
    - Uses a `try`/`finally` block to guarantee:
        - The `SENTINEL` is always enqueued.
        - Even if an exception occurs during iteration.

- **Shutdown Signal:**
    - Producer always pushes a unique sentinel object at the end.
    - This signals the consumer to shut down gracefully.

### 3. Consumer Thread

- **Responsibility:**
    - Continuously retrieves items from the queue and appends them to a destination list.

- **Key Features:**
    - Calls `queue.get()` in a loop.
    - On receiving the sentinel, exits cleanly.
    - Appends every non-sentinel item to the destination list.
    - Logs each consumed value.

- **Graceful Shutdown:**
    - Consumer stops only when it encounters the sentinel.
    - No busy loops. No extra flags.

### 4. Pipeline Orchestration (`run_pipeline()`)

- **Purpose:**
    - A convenience function that coordinates the entire flow.

- **Steps:**
    - Initializes a `BlockingQueue<T>` with the given capacity.
    - Creates:
        - One Producer thread.
        - One Consumer thread.
    - Starts both threads.
    - Waits for both to finish using `join()`.
    - Measures execution time.
    - Returns the final destination list.

- **Pipeline Flow:**
    `Source List` → `Producer` → `BlockingQueue<T>` → `Consumer` → `Destination List`

### 5. Sentinel Design

- **Concept:**
    - A unique object (`SENTINEL = object()`) is used to signal the end of the stream.

- **Benefits:**
    - It cannot collide with real data.
    - Identity (`is`) comparison is safe and fast.
    - Ensures clean termination of the consumer thread.
    - Avoids special-case logic for values like `None`.

## ▶️ Running the Program

### 1. Clone the repo

```bash
git clone https://github.com/tejas100/intuit-build-challenge-python
cd intuit-build-challenge-python/assignment1
```
### 2. Run the script

```bash
python producer_consumer.py
```
### Sample Output

```bash
[Producer] Produced: 1 | Queue size: 1
[Consumer] Consumed: 1 | Queue size: 0
[Producer] Produced: 2 | Queue size: 1
[Consumer] Consumed: 2 | Queue size: 0
[Producer] Produced: None | Queue size: 1
[Consumer] Consumed: None | Queue size: 0
[Producer] Produced: 4 | Queue size: 1
[Consumer] Consumed: 4 | Queue size: 0
[Producer] Sentinel sent.
[Consumer] Received sentinel. Exiting.

=== Pipeline Summary ===
Produced:  4 items
Consumed:  4 items
Time:      0.0002s
```

### 3. Running the tests

```bash
pytest -v
```
### Test results

```bash
(.venv) (base) tejas@Tejass-MacBook assignment1 % pytest -v                  
========================================= test session starts ==========================================
platform darwin -- Python 3.11.5, pytest-7.4.0, pluggy-1.0.0 -- /Users/temp/anaconda3/bin/python
cachedir: .pytest_cache
rootdir: /Users/temp/Documents/Projects/intuit-build-challenge-python/assignment1
plugins: anyio-3.5.0
collected 14 items                                                                                     

test_producer_consumer.py::test_queue_initial_size PASSED                                        [  7%]
test_producer_consumer.py::test_queue_put_and_get PASSED                                         [ 14%]
test_producer_consumer.py::test_queue_reject_zero_size PASSED                                    [ 21%]
test_producer_consumer.py::test_queue_blocks_when_empty PASSED                                   [ 28%]
test_producer_consumer.py::test_queue_blocks_when_full PASSED                                    [ 35%]
test_producer_consumer.py::test_sentinel_is_unique_and_safe PASSED                               [ 42%]
test_producer_consumer.py::test_producer_produces_items_and_sentinel PASSED                      [ 50%]
test_producer_consumer.py::test_producer_exception_still_sends_sentinel PASSED                   [ 57%]
test_producer_consumer.py::test_consumer_consumes_all_items PASSED                               [ 64%]
test_producer_consumer.py::test_consumer_stops_on_sentinel PASSED                                [ 71%]
test_producer_consumer.py::test_pipeline_simple_run PASSED                                       [ 78%]
test_producer_consumer.py::test_pipeline_with_none_values PASSED                                 [ 85%]
test_producer_consumer.py::test_large_pipeline PASSED                                            [ 92%]
test_producer_consumer.py::test_pipeline_queue_capacity_stress PASSED                            [100%]

========================================== 14 passed in 0.24s ==========================================
```

### Architecture

         ┌───────────────────┐         ┌──────────────────────────────┐         ┌─────────────────────┐
         │      Source       │         │        BlockingQueue<T>      │         │     Destination     │
         │       (List)      │         │        (max_size bounded)    │         │        (List)       │
         └─────────┬─────────┘         │  • Lock                      │         └─────────┬──────────-┘
                   │ Produces          │  • not_full Condition        │                   ▲ Consumes
                   ▼                   │  • not_empty Condition       │                   │
         ┌───────────────────┐         └──────────────────────────────┘         ┌─────────────────────┐
         │     Producer      │────────────────────────────────────────────────▶ │      Consumer       │
         └───────────────────┘                                                  └─────────────────────┘






