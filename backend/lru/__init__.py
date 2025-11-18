"""
Advanced LRU Cache System
~~~~~~~~~~~~~~~~~~~~~~~~~

A production-grade LRU cache implementation with TTL support,
thread safety, and comprehensive monitoring.
"""

from .lru_cache import LRUCache
from .lru_cache_ttl import LRUCacheTTL
from .lru_cache_threadsafe import ThreadSafeLRUCache
from .data_models import CacheEntry, CacheStats, CacheItem
from .logger import setup_logger, get_logger

__version__ = "1.0.0"
__all__ = [
    "LRUCache",
    "LRUCacheTTL",
    "ThreadSafeLRUCache",
    "CacheEntry",
    "CacheStats",
    "CacheItem",
    "setup_logger",
    "get_logger",
]
