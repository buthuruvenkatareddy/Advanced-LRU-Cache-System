"""
Unit tests for LRU Cache with TTL
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Test suite for TTL (Time-To-Live) functionality.
"""

import pytest
import time
from datetime import datetime
from lru import LRUCacheTTL, setup_logger


@pytest.fixture
def cache():
    """Create a fresh cache instance with TTL support."""
    setup_logger()
    return LRUCacheTTL(capacity=3, default_ttl=None)


@pytest.fixture
def cache_with_default_ttl():
    """Create cache with default TTL."""
    setup_logger()
    return LRUCacheTTL(capacity=3, default_ttl=2)


def test_ttl_initialization():
    """Test TTL cache initialization."""
    cache = LRUCacheTTL(capacity=5, default_ttl=10)
    assert cache.capacity == 5
    assert cache.default_ttl == 10


def test_ttl_invalid_default():
    """Test initialization with invalid default TTL."""
    with pytest.raises(ValueError):
        LRUCacheTTL(capacity=5, default_ttl=0)
    
    with pytest.raises(ValueError):
        LRUCacheTTL(capacity=5, default_ttl=-1)


def test_put_with_ttl(cache):
    """Test putting item with specific TTL."""
    cache.put("key1", "value1", ttl=1)
    assert cache.get("key1") == "value1"


def test_ttl_expiration(cache):
    """Test that items expire after TTL."""
    cache.put("key1", "value1", ttl=1)
    assert cache.get("key1") == "value1"
    
    # Wait for expiration
    time.sleep(1.1)
    
    # Should be expired and return None
    assert cache.get("key1") is None


def test_ttl_not_expired(cache):
    """Test that items don't expire before TTL."""
    cache.put("key1", "value1", ttl=5)
    
    # Wait but not long enough to expire
    time.sleep(0.5)
    
    # Should still be available
    assert cache.get("key1") == "value1"


def test_default_ttl_used(cache_with_default_ttl):
    """Test that default TTL is applied when not specified."""
    cache_with_default_ttl.put("key1", "value1")
    assert cache_with_default_ttl.get("key1") == "value1"
    
    # Wait for default TTL expiration
    time.sleep(2.1)
    
    assert cache_with_default_ttl.get("key1") is None


def test_ttl_override_default(cache_with_default_ttl):
    """Test that specific TTL overrides default."""
    cache_with_default_ttl.put("key1", "value1", ttl=10)
    
    # Wait past default TTL
    time.sleep(2.1)
    
    # Should still be available (10s TTL)
    assert cache_with_default_ttl.get("key1") == "value1"


def test_no_ttl_no_expiration(cache):
    """Test that items without TTL don't expire."""
    cache.put("key1", "value1")
    
    time.sleep(1)
    
    # Should still be available
    assert cache.get("key1") == "value1"


def test_cleanup_expired(cache):
    """Test manual cleanup of expired entries."""
    cache.put("key1", "value1", ttl=1)
    cache.put("key2", "value2", ttl=10)
    cache.put("key3", "value3")
    
    time.sleep(1.1)
    
    # Manually cleanup expired
    removed = cache.cleanup_expired()
    
    assert removed == 1
    assert cache.get("key1") is None
    assert cache.get("key2") == "value2"
    assert cache.get("key3") == "value3"


def test_expiration_statistics(cache):
    """Test that expirations are counted in statistics."""
    cache.put("key1", "value1", ttl=1)
    
    time.sleep(1.1)
    
    # Access expired key (should increment expiration count)
    cache.get("key1")
    
    stats = cache.get_stats()
    assert stats.expirations == 1


def test_update_ttl_on_existing_key(cache):
    """Test updating TTL of existing key."""
    cache.put("key1", "value1", ttl=1)
    
    # Update with new TTL
    cache.put("key1", "updated", ttl=10)
    
    # Wait past original TTL
    time.sleep(1.1)
    
    # Should still be available with new TTL
    assert cache.get("key1") == "updated"


def test_mixed_ttl_and_no_ttl(cache):
    """Test mix of items with and without TTL."""
    cache.put("key1", "value1", ttl=1)
    cache.put("key2", "value2")
    
    time.sleep(1.1)
    
    assert cache.get("key1") is None  # Expired
    assert cache.get("key2") == "value2"  # Still available


def test_ttl_eviction_interaction(cache):
    """Test interaction between TTL and LRU eviction."""
    cache.put("key1", "value1", ttl=1)
    cache.put("key2", "value2", ttl=10)
    cache.put("key3", "value3", ttl=10)
    
    # Wait for key1 to expire
    time.sleep(1.1)
    
    # Add key4, should evict based on LRU (key2 is least recent among non-expired)
    cache.put("key4", "value4")
    
    assert cache.get("key1") is None  # Expired
    assert cache.get("key2") is None  # Evicted
    assert cache.get("key3") == "value3"
    assert cache.get("key4") == "value4"


def test_get_all_items_with_ttl(cache):
    """Test getting all items includes TTL metadata."""
    cache.put("key1", "value1", ttl=10)
    cache.put("key2", "value2")
    
    items = cache.get_all_items()
    
    # Find key1 in items
    key1_item = next(item for item in items if item.key == "key1")
    assert key1_item.ttl == 10
    assert key1_item.expires_at is not None
    
    # Find key2 in items
    key2_item = next(item for item in items if item.key == "key2")
    assert key2_item.ttl is None
    assert key2_item.expires_at is None


def test_invalid_ttl_value(cache):
    """Test handling of invalid TTL values."""
    assert cache.put("key1", "value1", ttl=0) is False
    assert cache.put("key2", "value2", ttl=-1) is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
