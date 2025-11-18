"""
Unit tests for LRU Cache
~~~~~~~~~~~~~~~~~~~~~~~~~

Comprehensive test suite for core LRU cache functionality.
"""

import pytest
import time
from lru import LRUCache, setup_logger


@pytest.fixture
def cache():
    """Create a fresh cache instance for each test."""
    setup_logger()
    return LRUCache(capacity=3)


def test_cache_initialization():
    """Test cache initialization with valid capacity."""
    cache = LRUCache(capacity=5)
    assert cache.capacity == 5
    assert len(cache) == 0


def test_cache_invalid_capacity():
    """Test cache initialization with invalid capacity."""
    with pytest.raises(ValueError):
        LRUCache(capacity=0)
    
    with pytest.raises(ValueError):
        LRUCache(capacity=-1)


def test_put_and_get(cache):
    """Test basic put and get operations."""
    assert cache.put("key1", "value1") is True
    assert cache.get("key1") == "value1"


def test_get_nonexistent_key(cache):
    """Test getting a non-existent key."""
    assert cache.get("nonexistent") is None


def test_update_existing_key(cache):
    """Test updating an existing key."""
    cache.put("key1", "value1")
    cache.put("key1", "value2")
    assert cache.get("key1") == "value2"
    assert len(cache) == 1


def test_lru_eviction(cache):
    """Test LRU eviction when capacity is exceeded."""
    cache.put("key1", "value1")
    cache.put("key2", "value2")
    cache.put("key3", "value3")
    
    # Cache is full (capacity=3)
    assert len(cache) == 3
    
    # Add 4th item, should evict key1 (least recently used)
    cache.put("key4", "value4")
    
    assert len(cache) == 3
    assert cache.get("key1") is None  # Evicted
    assert cache.get("key2") == "value2"
    assert cache.get("key3") == "value3"
    assert cache.get("key4") == "value4"


def test_lru_order_on_access(cache):
    """Test that accessing a key updates its position in LRU order."""
    cache.put("key1", "value1")
    cache.put("key2", "value2")
    cache.put("key3", "value3")
    
    # Access key1 (moves it to front)
    cache.get("key1")
    
    # Add key4, should evict key2 (now least recently used)
    cache.put("key4", "value4")
    
    assert cache.get("key1") == "value1"  # Not evicted
    assert cache.get("key2") is None  # Evicted
    assert cache.get("key3") == "value3"
    assert cache.get("key4") == "value4"


def test_lru_order_on_update(cache):
    """Test that updating a key updates its position in LRU order."""
    cache.put("key1", "value1")
    cache.put("key2", "value2")
    cache.put("key3", "value3")
    
    # Update key1 (moves it to front)
    cache.put("key1", "updated")
    
    # Add key4, should evict key2 (now least recently used)
    cache.put("key4", "value4")
    
    assert cache.get("key1") == "updated"  # Not evicted
    assert cache.get("key2") is None  # Evicted
    assert cache.get("key3") == "value3"
    assert cache.get("key4") == "value4"


def test_delete(cache):
    """Test delete operation."""
    cache.put("key1", "value1")
    assert cache.delete("key1") is True
    assert cache.get("key1") is None
    assert len(cache) == 0


def test_delete_nonexistent(cache):
    """Test deleting a non-existent key."""
    assert cache.delete("nonexistent") is False


def test_clear(cache):
    """Test clear operation."""
    cache.put("key1", "value1")
    cache.put("key2", "value2")
    cache.put("key3", "value3")
    
    cache.clear()
    
    assert len(cache) == 0
    assert cache.get("key1") is None
    assert cache.get("key2") is None
    assert cache.get("key3") is None


def test_statistics(cache):
    """Test cache statistics tracking."""
    # Initial stats
    stats = cache.get_stats()
    assert stats.hits == 0
    assert stats.misses == 0
    assert stats.evictions == 0
    
    # Perform operations
    cache.put("key1", "value1")
    cache.get("key1")  # Hit
    cache.get("key2")  # Miss
    
    stats = cache.get_stats()
    assert stats.hits == 1
    assert stats.misses == 1
    assert stats.total_requests == 2
    assert stats.active_keys == 1


def test_eviction_statistics(cache):
    """Test eviction counting in statistics."""
    cache.put("key1", "value1")
    cache.put("key2", "value2")
    cache.put("key3", "value3")
    cache.put("key4", "value4")  # Triggers eviction
    
    stats = cache.get_stats()
    assert stats.evictions == 1


def test_get_all_items(cache):
    """Test retrieving all cache items."""
    cache.put("key1", "value1")
    cache.put("key2", "value2")
    
    items = cache.get_all_items()
    assert len(items) == 2
    
    keys = [item.key for item in items]
    assert "key1" in keys
    assert "key2" in keys


def test_contains(cache):
    """Test __contains__ magic method."""
    cache.put("key1", "value1")
    
    assert "key1" in cache
    assert "key2" not in cache


def test_len(cache):
    """Test __len__ magic method."""
    assert len(cache) == 0
    
    cache.put("key1", "value1")
    assert len(cache) == 1
    
    cache.put("key2", "value2")
    assert len(cache) == 2


def test_invalid_key_empty_string(cache):
    """Test handling of empty string key."""
    assert cache.put("", "value") is False
    assert cache.get("") is None


def test_invalid_key_whitespace(cache):
    """Test handling of whitespace-only key."""
    assert cache.put("   ", "value") is False
    assert cache.get("   ") is None


def test_various_value_types(cache):
    """Test caching various data types."""
    # String
    cache.put("str", "hello")
    assert cache.get("str") == "hello"
    
    # Integer
    cache.put("int", 42)
    assert cache.get("int") == 42
    
    # List
    cache.put("list", [1, 2, 3])
    assert cache.get("list") == [1, 2, 3]
    
    # Dict
    cache.put("dict", {"a": 1, "b": 2})
    assert cache.get("dict") == {"a": 1, "b": 2}


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
