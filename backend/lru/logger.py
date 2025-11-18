"""
Logging configuration for LRU Cache System
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Provides structured logging for cache operations.
"""

import logging
import sys
from datetime import datetime
from typing import Optional


class CacheLogger:
    """Custom logger for cache operations."""

    def __init__(self, name: str = "lru_cache", level: int = logging.INFO):
        """Initialize cache logger."""
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        # Prevent duplicate handlers
        if not self.logger.handlers:
            # Console handler
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(level)
            
            # Formatter
            formatter = logging.Formatter(
                fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            console_handler.setFormatter(formatter)
            
            self.logger.addHandler(console_handler)

    def cache_hit(self, key: str, value: any = None) -> None:
        """Log cache hit event."""
        self.logger.info(f"CACHE_HIT | key={key} | value_retrieved=True")

    def cache_miss(self, key: str) -> None:
        """Log cache miss event."""
        self.logger.warning(f"CACHE_MISS | key={key} | value_retrieved=False")

    def eviction(self, key: str, reason: str = "capacity") -> None:
        """Log cache eviction event."""
        self.logger.info(f"EVICTION | key={key} | reason={reason}")

    def expiry(self, key: str) -> None:
        """Log cache expiry event."""
        self.logger.info(f"EXPIRY | key={key} | reason=ttl_expired")

    def invalid_key(self, key: str, reason: str = "not_found") -> None:
        """Log invalid key access."""
        self.logger.warning(f"INVALID_KEY | key={key} | reason={reason}")

    def error(self, operation: str, error: Exception) -> None:
        """Log internal errors."""
        self.logger.error(f"ERROR | operation={operation} | error={str(error)}", exc_info=True)

    def cache_operation(self, operation: str, key: str, success: bool = True) -> None:
        """Log general cache operations."""
        status = "SUCCESS" if success else "FAILED"
        self.logger.info(f"OPERATION | type={operation} | key={key} | status={status}")

    def stats_snapshot(self, stats: dict) -> None:
        """Log cache statistics snapshot."""
        self.logger.info(f"STATS_SNAPSHOT | {stats}")


# Global logger instance
_logger: Optional[CacheLogger] = None


def setup_logger(name: str = "lru_cache", level: int = logging.INFO) -> CacheLogger:
    """
    Set up and return the global cache logger.
    
    Args:
        name: Logger name
        level: Logging level
        
    Returns:
        CacheLogger instance
    """
    global _logger
    _logger = CacheLogger(name=name, level=level)
    return _logger


def get_logger() -> CacheLogger:
    """
    Get the global cache logger instance.
    
    Returns:
        CacheLogger instance
    """
    global _logger
    if _logger is None:
        _logger = setup_logger()
    return _logger
