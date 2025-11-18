"""
Utility functions for LRU Cache System
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Helper functions for cache operations.
"""

import sys
from typing import Any
from datetime import datetime, timedelta


def estimate_size(obj: Any) -> int:
    """
    Estimate the memory size of an object in bytes.
    
    Args:
        obj: Object to estimate size for
        
    Returns:
        Estimated size in bytes
    """
    return sys.getsizeof(obj)


def calculate_expiry(ttl_seconds: int) -> datetime:
    """
    Calculate expiry datetime from TTL.
    
    Args:
        ttl_seconds: Time-to-live in seconds
        
    Returns:
        Expiry datetime
    """
    return datetime.now() + timedelta(seconds=ttl_seconds)


def format_memory_size(bytes_size: int) -> str:
    """
    Format bytes into human-readable format.
    
    Args:
        bytes_size: Size in bytes
        
    Returns:
        Formatted string (e.g., "1.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} PB"


def validate_key(key: str) -> bool:
    """
    Validate cache key.
    
    Args:
        key: Cache key to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not isinstance(key, str):
        return False
    if not key or key.strip() == "":
        return False
    return True


def validate_ttl(ttl: int) -> bool:
    """
    Validate TTL value.
    
    Args:
        ttl: Time-to-live in seconds
        
    Returns:
        True if valid, False otherwise
    """
    if not isinstance(ttl, int):
        return False
    if ttl <= 0:
        return False
    return True
