"""
Thread-Safe LRU Cache with TTL Support
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Implements thread-safe LRU cache using locks to prevent race conditions.
"""

from typing import Any, Optional, List
import threading

from .lru_cache_ttl import LRUCacheTTL
from .data_models import CacheStats, CacheEntry


class ThreadSafeLRUCache(LRUCacheTTL):
    """
    Thread-safe LRU Cache with TTL support.
    
    Uses threading.Lock to ensure thread safety for all operations.
    Prevents race conditions in multi-threaded environments.
    """

    def __init__(self, capacity: int = 100, default_ttl: Optional[int] = None):
        """
        Initialize thread-safe LRU Cache.
        
        Args:
            capacity: Maximum number of items to store
            default_ttl: Default time-to-live in seconds (None = no expiry)
            
        Raises:
            ValueError: If capacity < 1 or default_ttl is invalid
        """
        super().__init__(capacity, default_ttl)
        self.lock = threading.Lock()
        self.logger.cache_operation(
            "INIT_THREADSAFE",
            f"capacity={capacity}, default_ttl={default_ttl}",
            success=True
        )

    def get(self, key: str) -> Optional[Any]:
        """
        Thread-safe get operation.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value if found and not expired, None otherwise
        """
        with self.lock:
            return super().get(key)

    def put(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """
        Thread-safe put operation.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time-to-live in seconds (overrides default_ttl)
            
        Returns:
            True if successful, False otherwise
        """
        with self.lock:
            return super().put(key, value, ttl)

    def delete(self, key: str) -> bool:
        """
        Thread-safe delete operation.
        
        Args:
            key: Cache key to delete
            
        Returns:
            True if deleted, False if key not found
        """
        with self.lock:
            return super().delete(key)

    def clear(self) -> None:
        """Thread-safe clear operation."""
        with self.lock:
            super().clear()

    def get_stats(self) -> CacheStats:
        """
        Thread-safe statistics retrieval.
        
        Returns:
            CacheStats object with current statistics
        """
        with self.lock:
            return super().get_stats()

    def get_all_items(self) -> List[CacheEntry]:
        """
        Thread-safe retrieval of all cache items.
        
        Returns:
            List of CacheEntry objects
        """
        with self.lock:
            return super().get_all_items()

    def cleanup_expired(self) -> int:
        """
        Thread-safe cleanup of expired entries.
        
        Returns:
            Number of expired entries removed
        """
        with self.lock:
            return super().cleanup_expired()

    def size(self) -> int:
        """
        Thread-safe size retrieval.
        
        Returns:
            Number of cached items
        """
        with self.lock:
            return super().size()

    def set_capacity(self, new_capacity: int) -> bool:
        """
        Thread-safe capacity update.
        
        Args:
            new_capacity: New cache capacity
            
        Returns:
            True if successful, False otherwise
        """
        if new_capacity < 1:
            self.logger.error("SET_CAPACITY", ValueError("Capacity must be at least 1"))
            return False
        
        with self.lock:
            try:
                old_capacity = self.capacity
                self.capacity = new_capacity
                self.stats.capacity = new_capacity
                
                # Evict excess items if new capacity is smaller
                while len(self.cache) > self.capacity:
                    lru_node = self._remove_tail()
                    del self.cache[lru_node.key]
                    
                    self.stats.evictions += 1
                    self.logger.eviction(lru_node.key, reason="capacity_reduced")
                
                self.stats.active_keys = len(self.cache)
                self.logger.cache_operation(
                    "SET_CAPACITY",
                    f"old={old_capacity}, new={new_capacity}",
                    success=True
                )
                return True
                
            except Exception as e:
                self.logger.error("SET_CAPACITY", e)
                return False

    def __contains__(self, key: str) -> bool:
        """Thread-safe containment check."""
        with self.lock:
            return super().__contains__(key)

    def __len__(self) -> int:
        """Thread-safe length."""
        with self.lock:
            return super().__len__()

    def __repr__(self) -> str:
        """String representation of cache."""
        with self.lock:
            return (
                f"ThreadSafeLRUCache(capacity={self.capacity}, size={len(self.cache)}, "
                f"default_ttl={self.default_ttl})"
            )
