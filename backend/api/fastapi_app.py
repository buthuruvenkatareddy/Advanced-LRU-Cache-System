"""
FastAPI Application for LRU Cache System
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

REST API for managing and monitoring the LRU cache.
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator
from typing import Optional, Any, List, Dict
from datetime import datetime
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lru import ThreadSafeLRUCache, setup_logger, CacheEntry


# Pydantic models for request/response validation
class CachePutRequest(BaseModel):
    """Request model for PUT cache operation."""
    key: str = Field(..., min_length=1, description="Cache key")
    value: Any = Field(..., description="Value to cache")
    ttl: Optional[int] = Field(None, gt=0, description="Time-to-live in seconds")

    @validator('key')
    def key_not_empty(cls, v):
        """Validate key is not empty."""
        if not v or v.strip() == "":
            raise ValueError('Key cannot be empty')
        return v


class CacheGetResponse(BaseModel):
    """Response model for GET cache operation."""
    key: str
    value: Any
    found: bool
    timestamp: str


class CacheDeleteResponse(BaseModel):
    """Response model for DELETE cache operation."""
    key: str
    deleted: bool
    message: str


class CacheStatsResponse(BaseModel):
    """Response model for cache statistics."""
    hits: int
    misses: int
    evictions: int
    expirations: int
    total_requests: int
    active_keys: int
    capacity: int
    memory_usage_bytes: int
    hit_rate: float
    miss_rate: float


class CacheItemResponse(BaseModel):
    """Response model for cache item."""
    key: str
    value: Any
    created_at: str
    last_accessed: str
    ttl: Optional[int]
    expires_at: Optional[str]
    access_count: int
    ttl_remaining: Optional[int] = None


class CapacityUpdateRequest(BaseModel):
    """Request model for capacity update."""
    capacity: int = Field(..., gt=0, description="New cache capacity")


class MessageResponse(BaseModel):
    """Generic message response."""
    message: str
    success: bool


# Initialize FastAPI app
app = FastAPI(
    title="Advanced LRU Cache System API",
    description="Production-grade LRU cache with TTL, thread safety, and monitoring",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize cache and logger
DEFAULT_CAPACITY = 100
DEFAULT_TTL = None
cache = ThreadSafeLRUCache(capacity=DEFAULT_CAPACITY, default_ttl=DEFAULT_TTL)
logger = setup_logger(name="lru_cache_api")


# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Handle all unhandled exceptions."""
    logger.error("UNHANDLED_EXCEPTION", exc)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error", "error": str(exc)}
    )


# API Endpoints
@app.get("/", tags=["Health"])
async def root():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Advanced LRU Cache System",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Detailed health check."""
    stats = cache.get_stats()
    return {
        "status": "healthy",
        "cache_active": True,
        "active_keys": stats.active_keys,
        "capacity": stats.capacity,
        "timestamp": datetime.now().isoformat()
    }


@app.get("/cache/{key}", response_model=CacheGetResponse, tags=["Cache Operations"])
async def get_cache_item(key: str):
    """
    Get value from cache by key.
    
    Args:
        key: Cache key
        
    Returns:
        Cached value if found
        
    Raises:
        HTTPException: If key not found
    """
    value = cache.get(key)
    
    if value is not None:
        return CacheGetResponse(
            key=key,
            value=value,
            found=True,
            timestamp=datetime.now().isoformat()
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Key '{key}' not found in cache"
        )


@app.post("/cache", response_model=MessageResponse, tags=["Cache Operations"])
async def put_cache_item(request: CachePutRequest):
    """
    Put key-value pair into cache.
    
    Args:
        request: CachePutRequest with key, value, and optional TTL
        
    Returns:
        Success message
        
    Raises:
        HTTPException: If operation fails
    """
    success = cache.put(request.key, request.value, request.ttl)
    
    if success:
        return MessageResponse(
            message=f"Key '{request.key}' successfully added to cache",
            success=True
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to add key to cache"
        )


@app.delete("/cache/{key}", response_model=CacheDeleteResponse, tags=["Cache Operations"])
async def delete_cache_item(key: str):
    """
    Delete key from cache.
    
    Args:
        key: Cache key to delete
        
    Returns:
        Deletion result
    """
    deleted = cache.delete(key)
    
    if deleted:
        return CacheDeleteResponse(
            key=key,
            deleted=True,
            message=f"Key '{key}' successfully deleted"
        )
    else:
        return CacheDeleteResponse(
            key=key,
            deleted=False,
            message=f"Key '{key}' not found in cache"
        )


@app.get("/stats", response_model=CacheStatsResponse, tags=["Monitoring"])
async def get_statistics():
    """
    Get cache statistics.
    
    Returns:
        Cache statistics including hits, misses, evictions, etc.
    """
    stats = cache.get_stats()
    return CacheStatsResponse(**stats.to_dict())


@app.get("/all", response_model=List[CacheItemResponse], tags=["Cache Operations"])
async def get_all_items():
    """
    Get all cache items with metadata.
    
    Returns:
        List of all cached items with metadata
    """
    items = cache.get_all_items()
    
    response_items = []
    for item in items:
        # Calculate TTL remaining
        ttl_remaining = None
        if item.expires_at:
            remaining_seconds = (item.expires_at - datetime.now()).total_seconds()
            ttl_remaining = max(0, int(remaining_seconds))
        
        response_items.append(
            CacheItemResponse(
                key=item.key,
                value=item.value,
                created_at=item.created_at.isoformat(),
                last_accessed=item.last_accessed.isoformat(),
                ttl=item.ttl,
                expires_at=item.expires_at.isoformat() if item.expires_at else None,
                access_count=item.access_count,
                ttl_remaining=ttl_remaining
            )
        )
    
    return response_items


@app.post("/clear", response_model=MessageResponse, tags=["Cache Operations"])
async def clear_cache():
    """
    Clear all items from cache.
    
    Returns:
        Success message
    """
    cache.clear()
    return MessageResponse(
        message="Cache successfully cleared",
        success=True
    )


@app.post("/cleanup-expired", response_model=MessageResponse, tags=["Cache Operations"])
async def cleanup_expired():
    """
    Manually cleanup expired entries.
    
    Returns:
        Number of expired entries removed
    """
    count = cache.cleanup_expired()
    return MessageResponse(
        message=f"Removed {count} expired entries",
        success=True
    )


@app.put("/capacity", response_model=MessageResponse, tags=["Configuration"])
async def update_capacity(request: CapacityUpdateRequest):
    """
    Update cache capacity.
    
    Args:
        request: New capacity value
        
    Returns:
        Success message
        
    Raises:
        HTTPException: If capacity update fails
    """
    success = cache.set_capacity(request.capacity)
    
    if success:
        return MessageResponse(
            message=f"Cache capacity updated to {request.capacity}",
            success=True
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to update cache capacity"
        )


@app.get("/cache-info", tags=["Monitoring"])
async def get_cache_info():
    """
    Get detailed cache configuration and status.
    
    Returns:
        Cache configuration and status information
    """
    stats = cache.get_stats()
    return {
        "capacity": cache.capacity,
        "default_ttl": cache.default_ttl,
        "current_size": len(cache),
        "statistics": stats.to_dict(),
        "thread_safe": True,
        "implementation": "HashMap + Doubly Linked List"
    }


# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Initialize cache on startup."""
    logger.cache_operation("API_STARTUP", "FastAPI application started", success=True)
    print(f"✅ LRU Cache API started successfully")
    print(f"📊 Cache capacity: {cache.capacity}")
    print(f"⏰ Default TTL: {cache.default_ttl or 'None'}")
    print(f"🔒 Thread-safe: Yes")
    print(f"📖 API docs: http://localhost:8000/docs")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.cache_operation("API_SHUTDOWN", "FastAPI application shutting down", success=True)
    print("👋 LRU Cache API shutting down...")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "fastapi_app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
