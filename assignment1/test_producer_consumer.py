import time
import threading
import pytest

from assignment1.producer_consumer import (
    BlockingQueue,
    Producer,
    Consumer,
    run_pipeline,
    SENTINEL,
)


# ============================================================
#                  TEST: BlockingQueue Behavior
# ============================================================


def test_queue_initial_size():
    q = BlockingQueue(max_size=5)
    assert q.size() == 0


def test_queue_put_and_get():
    q = BlockingQueue(max_size=5)
    q.put(10)
    q.put(20)

    assert q.size() == 2
    assert q.get() == 10
    assert q.get() == 20
    assert q.size() == 0


def test_queue_reject_zero_size():
    with pytest.raises(ValueError):
        BlockingQueue(max_size=0)


def test_queue_blocks_when_empty():
    q = BlockingQueue(max_size=5)
    results = []

    def consumer():
        item = q.get()
        results.append(item)

    t = threading.Thread(target=consumer)
    t.start()

    time.sleep(0.1)
    assert results == []

    q.put(99)
    t.join(timeout=1)

    assert results == [99]


def test_queue_blocks_when_full():
    q = BlockingQueue(max_size=2)
    q.put(1)
    q.put(2)

    blocked = True

    def producer():
        nonlocal blocked
        q.put(3)
        blocked = False

    t = threading.Thread(target=producer)
    t.start()

    time.sleep(0.1)
    assert blocked is True

    q.get()

    t.join(timeout=1)
    assert blocked is False
    assert q.size() == 2


def test_sentinel_is_unique_and_safe():
    assert SENTINEL is not None
    assert SENTINEL != None  
    assert SENTINEL is not object()


# ============================================================
#                     TEST: Producer Behavior
# ============================================================


def test_producer_produces_items_and_sentinel():
    q = BlockingQueue(max_size=10)
    source = [1, 2, 3]
    producer = Producer(source, q, SENTINEL)

    producer.start()
    producer.join(timeout=1)

    assert q.get() == 1
    assert q.get() == 2
    assert q.get() == 3
    assert q.get() is SENTINEL


# ============================================================
#                TEST: Producer Exception Handling
# ============================================================

def test_producer_exception_still_sends_sentinel():
    """
    Ensures the REAL Producer.run() finally block always sends the sentinel,
    even when iteration over the source fails.
    """

    class ExplodingIterable:
        def __iter__(self):
            yield 1
            yield 2
            raise RuntimeError("Simulated failure during iteration")
            yield 3  # never reached

    q = BlockingQueue(max_size=5)
    destination = []

    source = ExplodingIterable()

    producer = Producer(source, q, SENTINEL)
    consumer = Consumer(q, destination, SENTINEL)

    producer.start()
    consumer.start()

    producer.join(timeout=1)
    consumer.join(timeout=1)

    # The consumer must process only the successfully yielded values
    assert destination == [1, 2]

    # And must exit due to sentinel
    assert producer.is_alive() is False
    assert consumer.is_alive() is False

# ============================================================
#                     TEST: Consumer Behavior
# ============================================================


def test_consumer_consumes_all_items():
    q = BlockingQueue(max_size=10)
    destination = []

    q.put(5)
    q.put(10)
    q.put(SENTINEL)

    consumer = Consumer(q, destination, SENTINEL)

    consumer.start()
    consumer.join(timeout=1)

    assert destination == [5, 10]


def test_consumer_stops_on_sentinel():
    q = BlockingQueue(max_size=10)
    destination = []

    q.put(1)
    q.put(SENTINEL)
    q.put(999)

    consumer = Consumer(q, destination, SENTINEL)

    consumer.start()
    consumer.join(timeout=1)

    assert destination == [1]


# ============================================================
#                     TEST: Integration Pipeline
# ============================================================


def test_pipeline_simple_run():
    source = [1, 2, 3, 4, 5]
    result = run_pipeline(source)

    assert result == source


def test_pipeline_with_none_values():
    source = [1, None, 3]
    result = run_pipeline(source)

    assert result == [1, None, 3]


def test_large_pipeline():
    source = list(range(100))
    result = run_pipeline(source, queue_size=10)

    assert result == source


def test_pipeline_queue_capacity_stress():
    source = list(range(50))
    result = run_pipeline(source, queue_size=2)

    assert result == source
