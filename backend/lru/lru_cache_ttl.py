"""
LRU Cache with TTL (Time-To-Live) Support
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Extends LRU cache with automatic expiration of entries.
"""

from typing import Any, Optional
from datetime import datetime

from .lru_cache import LRUCache
from .data_models import CacheItem
from .utils import calculate_expiry, validate_ttl


class LRUCacheTTL(LRUCache):
    """
    LRU Cache with TTL (Time-To-Live) support.
    
    Extends base LRU cache to support automatic expiration of entries.
    Expired entries are removed lazily on access.
    """

    def __init__(self, capacity: int = 100, default_ttl: Optional[int] = None):
        """
        Initialize LRU Cache with TTL support.
        
        Args:
            capacity: Maximum number of items to store
            default_ttl: Default time-to-live in seconds (None = no expiry)
            
        Raises:
            ValueError: If capacity < 1 or default_ttl is invalid
        """
        super().__init__(capacity)
        
        if default_ttl is not None and not validate_ttl(default_ttl):
            raise ValueError("default_ttl must be a positive integer")
        
        self.default_ttl = default_ttl
        self.logger.cache_operation(
            "INIT_TTL",
            f"capacity={capacity}, default_ttl={default_ttl}",
            success=True
        )

    def _is_expired(self, node: CacheItem) -> bool:
        """
        Check if a cache item has expired.
        
        Args:
            node: CacheItem to check
            
        Returns:
            True if expired, False otherwise
        """
        return node.is_expired()

    def _remove_expired(self, key: str, node: CacheItem) -> None:
        """
        Remove expired cache item.
        
        Args:
            key: Cache key
            node: Expired CacheItem
        """
        self._remove_node(node)
        del self.cache[key]
        
        self.stats.expirations += 1
        self.stats.active_keys = len(self.cache)
        self.logger.expiry(key)

    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache by key, checking for expiration.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value if found and not expired, None otherwise
        """
        from .utils import validate_key
        
        if not validate_key(key):
            self.logger.invalid_key(key, reason="invalid_format")
            return None
        
        self.stats.total_requests += 1
        
        if key in self.cache:
            node = self.cache[key]
            
            # Check if expired
            if self._is_expired(node):
                self._remove_expired(key, node)
                self.stats.misses += 1
                self.logger.cache_miss(key)
                return None
            
            # Not expired, update and return
            node.update_access()
            self._move_to_head(node)
            
            self.stats.hits += 1
            self.logger.cache_hit(key, node.value)
            return node.value
        else:
            self.stats.misses += 1
            self.logger.cache_miss(key)
            return None

    def put(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """
        Put key-value pair into cache with optional TTL.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time-to-live in seconds (overrides default_ttl)
            
        Returns:
            True if successful, False otherwise
        """
        from .utils import validate_key
        
        if not validate_key(key):
            self.logger.invalid_key(key, reason="invalid_format")
            return False
        
        # Use provided TTL, fall back to default, or None
        effective_ttl = ttl if ttl is not None else self.default_ttl
        
        if effective_ttl is not None and not validate_ttl(effective_ttl):
            self.logger.error("PUT", ValueError(f"Invalid TTL: {effective_ttl}"))
            return False
        
        try:
            if key in self.cache:
                # Update existing key
                node = self.cache[key]
                node.value = value
                node.ttl = effective_ttl
                node.expires_at = calculate_expiry(effective_ttl) if effective_ttl else None
                node.update_access()
                self._move_to_head(node)
                self.logger.cache_operation("UPDATE_TTL", key, success=True)
            else:
                # Add new key
                expires_at = calculate_expiry(effective_ttl) if effective_ttl else None
                new_node = CacheItem(
                    key=key,
                    value=value,
                    ttl=effective_ttl,
                    expires_at=expires_at
                )
                self.cache[key] = new_node
                self._add_to_head(new_node)
                
                # Check capacity and evict if necessary
                if len(self.cache) > self.capacity:
                    lru_node = self._remove_tail()
                    del self.cache[lru_node.key]
                    
                    self.stats.evictions += 1
                    self.logger.eviction(lru_node.key, reason="capacity")
                
                self.stats.active_keys = len(self.cache)
                self.logger.cache_operation("PUT_TTL", key, success=True)
            
            return True
            
        except Exception as e:
            self.logger.error("PUT_TTL", e)
            return False

    def cleanup_expired(self) -> int:
        """
        Manually cleanup all expired entries.
        
        Returns:
            Number of expired entries removed
        """
        expired_keys = []
        
        for key, node in self.cache.items():
            if self._is_expired(node):
                expired_keys.append(key)
        
        for key in expired_keys:
            node = self.cache[key]
            self._remove_node(node)
            del self.cache[key]
            
            self.stats.expirations += 1
            self.logger.expiry(key)
        
        self.stats.active_keys = len(self.cache)
        
        if expired_keys:
            self.logger.cache_operation(
                "CLEANUP_EXPIRED",
                f"removed={len(expired_keys)}",
                success=True
            )
        
        return len(expired_keys)

    def __repr__(self) -> str:
        """String representation of cache."""
        return (
            f"LRUCacheTTL(capacity={self.capacity}, size={len(self.cache)}, "
            f"default_ttl={self.default_ttl})"
        )
