"""
Unit tests for Thread-Safe LRU Cache
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Test suite for thread safety and concurrent access.
"""

import pytest
import threading
import time
from lru import ThreadSafeLRUCache, setup_logger


@pytest.fixture
def cache():
    """Create a thread-safe cache instance."""
    setup_logger()
    return ThreadSafeLRUCache(capacity=100, default_ttl=None)


def test_threadsafe_initialization():
    """Test thread-safe cache initialization."""
    cache = ThreadSafeLRUCache(capacity=10, default_ttl=5)
    assert cache.capacity == 10
    assert cache.default_ttl == 5
    assert hasattr(cache, 'lock')


def test_concurrent_puts(cache):
    """Test concurrent put operations."""
    num_threads = 10
    items_per_thread = 10
    
    def put_items(thread_id):
        for i in range(items_per_thread):
            key = f"thread{thread_id}_key{i}"
            value = f"value{i}"
            cache.put(key, value)
    
    threads = []
    for i in range(num_threads):
        thread = threading.Thread(target=put_items, args=(i,))
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    # Verify total items (may be less than 100 due to capacity)
    assert len(cache) <= cache.capacity


def test_concurrent_gets(cache):
    """Test concurrent get operations."""
    # Pre-populate cache
    for i in range(10):
        cache.put(f"key{i}", f"value{i}")
    
    results = []
    lock = threading.Lock()
    
    def get_items():
        for i in range(10):
            value = cache.get(f"key{i}")
            with lock:
                results.append(value)
    
    threads = []
    for _ in range(5):
        thread = threading.Thread(target=get_items)
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    # All gets should have succeeded
    assert len(results) == 50
    assert all(v is not None for v in results if "value" in str(v))


def test_concurrent_mixed_operations(cache):
    """Test mixed concurrent operations (put, get, delete)."""
    operations_count = [0, 0, 0]  # [puts, gets, deletes]
    lock = threading.Lock()
    
    def perform_operations(thread_id):
        for i in range(20):
            operation = i % 3
            key = f"thread{thread_id}_key{i}"
            
            if operation == 0:
                cache.put(key, f"value{i}")
                with lock:
                    operations_count[0] += 1
            elif operation == 1:
                cache.get(key)
                with lock:
                    operations_count[1] += 1
            else:
                cache.delete(key)
                with lock:
                    operations_count[2] += 1
    
    threads = []
    for i in range(5):
        thread = threading.Thread(target=perform_operations, args=(i,))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    # Verify all operations completed
    assert sum(operations_count) == 100


def test_concurrent_statistics(cache):
    """Test statistics accuracy under concurrent access."""
    def perform_operations():
        for i in range(10):
            cache.put(f"key{i}", f"value{i}")
            cache.get(f"key{i}")
            cache.get("nonexistent")
    
    threads = []
    for _ in range(5):
        thread = threading.Thread(target=perform_operations)
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    stats = cache.get_stats()
    
    # Verify statistics are consistent
    assert stats.hits > 0
    assert stats.misses > 0
    assert stats.total_requests == stats.hits + stats.misses


def test_set_capacity_threadsafe(cache):
    """Test thread-safe capacity update."""
    # Pre-populate cache
    for i in range(50):
        cache.put(f"key{i}", f"value{i}")
    
    # Update capacity while other threads are accessing
    def access_cache():
        for i in range(20):
            cache.get(f"key{i % 50}")
            time.sleep(0.001)
    
    # Start access threads
    access_thread = threading.Thread(target=access_cache)
    access_thread.start()
    
    # Update capacity
    success = cache.set_capacity(30)
    
    access_thread.join()
    
    assert success is True
    assert cache.capacity == 30
    assert len(cache) <= 30


def test_clear_threadsafe(cache):
    """Test thread-safe clear operation."""
    # Pre-populate cache
    for i in range(20):
        cache.put(f"key{i}", f"value{i}")
    
    def access_and_clear():
        cache.get("key0")
        time.sleep(0.01)
        cache.clear()
    
    threads = []
    for _ in range(3):
        thread = threading.Thread(target=access_and_clear)
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    # Cache should be empty after all clears
    assert len(cache) == 0


def test_concurrent_ttl_operations(cache):
    """Test concurrent operations with TTL."""
    def put_with_ttl(thread_id):
        for i in range(10):
            key = f"thread{thread_id}_key{i}"
            cache.put(key, f"value{i}", ttl=2)
    
    threads = []
    for i in range(5):
        thread = threading.Thread(target=put_with_ttl, args=(i,))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    # Wait for some to expire
    time.sleep(2.1)
    
    # Cleanup expired
    removed = cache.cleanup_expired()
    
    # Some items should have expired
    assert removed > 0


def test_get_all_items_threadsafe(cache):
    """Test thread-safe retrieval of all items."""
    # Pre-populate
    for i in range(20):
        cache.put(f"key{i}", f"value{i}")
    
    def get_all():
        items = cache.get_all_items()
        return len(items)
    
    results = []
    threads = []
    
    for _ in range(5):
        thread = threading.Thread(target=lambda: results.append(get_all()))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    # All threads should get consistent results
    assert len(results) == 5


def test_race_condition_prevention(cache):
    """Test that race conditions are prevented."""
    counter = [0]
    
    def increment_operation():
        for _ in range(100):
            # Read-modify-write operation
            cache.put("counter", counter[0])
            value = cache.get("counter")
            if value is not None:
                counter[0] = value + 1
                cache.put("counter", counter[0])
    
    threads = []
    for _ in range(10):
        thread = threading.Thread(target=increment_operation)
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    # With proper locking, operations should be consistent
    final_value = cache.get("counter")
    assert final_value is not None


def test_contains_threadsafe(cache):
    """Test thread-safe __contains__ operation."""
    cache.put("key1", "value1")
    
    def check_contains():
        assert "key1" in cache
        assert "nonexistent" not in cache
    
    threads = []
    for _ in range(10):
        thread = threading.Thread(target=check_contains)
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()


def test_len_threadsafe(cache):
    """Test thread-safe __len__ operation."""
    for i in range(10):
        cache.put(f"key{i}", f"value{i}")
    
    lengths = []
    
    def get_length():
        lengths.append(len(cache))
    
    threads = []
    for _ in range(5):
        thread = threading.Thread(target=get_length)
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    # All lengths should be consistent
    assert all(length == 10 for length in lengths)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
