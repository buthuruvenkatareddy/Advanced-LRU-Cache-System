"""
Data models for LRU Cache System
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Defines data structures and type hints for cache operations.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional, Dict


@dataclass
class CacheEntry:
    """Represents a single cache entry with metadata."""
    
    key: str
    value: Any
    created_at: datetime = field(default_factory=datetime.now)
    last_accessed: datetime = field(default_factory=datetime.now)
    ttl: Optional[int] = None  # Time-to-live in seconds
    expires_at: Optional[datetime] = None
    access_count: int = 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert entry to dictionary format."""
        return {
            "key": self.key,
            "value": self.value,
            "created_at": self.created_at.isoformat(),
            "last_accessed": self.last_accessed.isoformat(),
            "ttl": self.ttl,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "access_count": self.access_count,
        }


@dataclass
class CacheStats:
    """Statistics for cache performance monitoring."""
    
    hits: int = 0
    misses: int = 0
    evictions: int = 0
    expirations: int = 0
    total_requests: int = 0
    active_keys: int = 0
    capacity: int = 0
    memory_usage_bytes: int = 0

    @property
    def hit_rate(self) -> float:
        """Calculate cache hit rate as percentage."""
        if self.total_requests == 0:
            return 0.0
        return (self.hits / self.total_requests) * 100

    @property
    def miss_rate(self) -> float:
        """Calculate cache miss rate as percentage."""
        if self.total_requests == 0:
            return 0.0
        return (self.misses / self.total_requests) * 100

    def to_dict(self) -> Dict[str, Any]:
        """Convert stats to dictionary format."""
        return {
            "hits": self.hits,
            "misses": self.misses,
            "evictions": self.evictions,
            "expirations": self.expirations,
            "total_requests": self.total_requests,
            "active_keys": self.active_keys,
            "capacity": self.capacity,
            "memory_usage_bytes": self.memory_usage_bytes,
            "hit_rate": round(self.hit_rate, 2),
            "miss_rate": round(self.miss_rate, 2),
        }


@dataclass
class CacheItem:
    """Internal node for doubly linked list."""
    
    key: str
    value: Any
    ttl: Optional[int] = None
    expires_at: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.now)
    last_accessed: datetime = field(default_factory=datetime.now)
    access_count: int = 0
    prev: Optional['CacheItem'] = None
    next: Optional['CacheItem'] = None

    def is_expired(self) -> bool:
        """Check if the cache item has expired."""
        if self.expires_at is None:
            return False
        return datetime.now() > self.expires_at

    def update_access(self) -> None:
        """Update access metadata."""
        self.last_accessed = datetime.now()
        self.access_count += 1
