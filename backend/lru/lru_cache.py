"""
Core LRU Cache Implementation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Implements LRU cache using HashMap + Doubly Linked List for O(1) operations.
"""

from typing import Any, Optional, Dict, List
from datetime import datetime

from .data_models import CacheItem, CacheStats, CacheEntry
from .logger import get_logger
from .utils import estimate_size, validate_key


class LRUCache:
    """
    LRU (Least Recently Used) Cache implementation.
    
    Uses a HashMap for O(1) lookups and a Doubly Linked List
    for O(1) eviction of least recently used items.
    
    Attributes:
        capacity: Maximum number of items the cache can hold
        cache: HashMap storing key -> CacheItem mappings
        head: Dummy head node of doubly linked list (most recent)
        tail: Dummy tail node of doubly linked list (least recent)
        stats: Cache statistics tracker
    """

    def __init__(self, capacity: int = 100):
        """
        Initialize LRU Cache.
        
        Args:
            capacity: Maximum number of items to store
            
        Raises:
            ValueError: If capacity is less than 1
        """
        if capacity < 1:
            raise ValueError("Capacity must be at least 1")
        
        self.capacity = capacity
        self.cache: Dict[str, CacheItem] = {}
        self.logger = get_logger()
        
        # Initialize doubly linked list with dummy head and tail
        self.head = CacheItem(key="HEAD", value=None)
        self.tail = CacheItem(key="TAIL", value=None)
        self.head.next = self.tail
        self.tail.prev = self.head
        
        # Statistics
        self.stats = CacheStats(capacity=capacity)
        
        self.logger.cache_operation("INIT", f"capacity={capacity}", success=True)

    def _add_to_head(self, node: CacheItem) -> None:
        """
        Add node right after head (most recently used position).
        
        Args:
            node: CacheItem to add
        """
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _remove_node(self, node: CacheItem) -> None:
        """
        Remove node from doubly linked list.
        
        Args:
            node: CacheItem to remove
        """
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def _move_to_head(self, node: CacheItem) -> None:
        """
        Move existing node to head (mark as most recently used).
        
        Args:
            node: CacheItem to move
        """
        self._remove_node(node)
        self._add_to_head(node)

    def _remove_tail(self) -> CacheItem:
        """
        Remove and return the least recently used item (before tail).
        
        Returns:
            The removed CacheItem
        """
        lru_node = self.tail.prev
        self._remove_node(lru_node)
        return lru_node

    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache by key.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value if found, None otherwise
        """
        if not validate_key(key):
            self.logger.invalid_key(key, reason="invalid_format")
            return None
        
        self.stats.total_requests += 1
        
        if key in self.cache:
            node = self.cache[key]
            node.update_access()
            self._move_to_head(node)
            
            self.stats.hits += 1
            self.logger.cache_hit(key, node.value)
            return node.value
        else:
            self.stats.misses += 1
            self.logger.cache_miss(key)
            return None

    def put(self, key: str, value: Any) -> bool:
        """
        Put key-value pair into cache.
        
        Args:
            key: Cache key
            value: Value to cache
            
        Returns:
            True if successful, False otherwise
        """
        if not validate_key(key):
            self.logger.invalid_key(key, reason="invalid_format")
            return False
        
        try:
            if key in self.cache:
                # Update existing key
                node = self.cache[key]
                node.value = value
                node.update_access()
                self._move_to_head(node)
                self.logger.cache_operation("UPDATE", key, success=True)
            else:
                # Add new key
                new_node = CacheItem(key=key, value=value)
                self.cache[key] = new_node
                self._add_to_head(new_node)
                
                # Check capacity and evict if necessary
                if len(self.cache) > self.capacity:
                    lru_node = self._remove_tail()
                    del self.cache[lru_node.key]
                    
                    self.stats.evictions += 1
                    self.logger.eviction(lru_node.key, reason="capacity")
                
                self.stats.active_keys = len(self.cache)
                self.logger.cache_operation("PUT", key, success=True)
            
            return True
            
        except Exception as e:
            self.logger.error("PUT", e)
            return False

    def delete(self, key: str) -> bool:
        """
        Delete key from cache.
        
        Args:
            key: Cache key to delete
            
        Returns:
            True if deleted, False if key not found
        """
        if not validate_key(key):
            self.logger.invalid_key(key, reason="invalid_format")
            return False
        
        if key in self.cache:
            node = self.cache[key]
            self._remove_node(node)
            del self.cache[key]
            
            self.stats.active_keys = len(self.cache)
            self.logger.cache_operation("DELETE", key, success=True)
            return True
        else:
            self.logger.invalid_key(key, reason="not_found")
            return False

    def clear(self) -> None:
        """Clear all items from cache."""
        self.cache.clear()
        self.head.next = self.tail
        self.tail.prev = self.head
        self.stats.active_keys = 0
        self.logger.cache_operation("CLEAR", "all", success=True)

    def get_stats(self) -> CacheStats:
        """
        Get current cache statistics.
        
        Returns:
            CacheStats object with current statistics
        """
        self.stats.active_keys = len(self.cache)
        self.stats.memory_usage_bytes = sum(
            estimate_size(node.key) + estimate_size(node.value)
            for node in self.cache.values()
        )
        return self.stats

    def get_all_items(self) -> List[CacheEntry]:
        """
        Get all cache items with metadata.
        
        Returns:
            List of CacheEntry objects
        """
        items = []
        for node in self.cache.values():
            entry = CacheEntry(
                key=node.key,
                value=node.value,
                created_at=node.created_at,
                last_accessed=node.last_accessed,
                access_count=node.access_count,
                ttl=node.ttl,
                expires_at=node.expires_at
            )
            items.append(entry)
        return items

    def size(self) -> int:
        """
        Get current number of items in cache.
        
        Returns:
            Number of cached items
        """
        return len(self.cache)

    def __len__(self) -> int:
        """Return the number of items in cache."""
        return len(self.cache)

    def __contains__(self, key: str) -> bool:
        """Check if key exists in cache."""
        return key in self.cache

    def __repr__(self) -> str:
        """String representation of cache."""
        return f"LRUCache(capacity={self.capacity}, size={len(self.cache)})"
