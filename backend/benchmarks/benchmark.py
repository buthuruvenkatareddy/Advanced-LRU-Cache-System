"""
Performance benchmarks for LRU Cache
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Benchmark suite to measure cache performance.
"""

import time
import random
import string
from typing import List, Tuple
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lru import LRUCache, LRUCacheTTL, ThreadSafeLRUCache, setup_logger


def generate_random_string(length: int = 10) -> str:
    """Generate a random string."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def benchmark_put_operations(cache, num_operations: int = 10000) -> float:
    """Benchmark PUT operations."""
    start_time = time.time()
    
    for i in range(num_operations):
        key = f"key{i}"
        value = f"value{i}"
        cache.put(key, value)
    
    end_time = time.time()
    return end_time - start_time


def benchmark_get_operations(cache, num_operations: int = 10000) -> float:
    """Benchmark GET operations."""
    # Pre-populate cache
    for i in range(min(num_operations, cache.capacity)):
        cache.put(f"key{i}", f"value{i}")
    
    start_time = time.time()
    
    for i in range(num_operations):
        key = f"key{i % cache.capacity}"
        cache.get(key)
    
    end_time = time.time()
    return end_time - start_time


def benchmark_mixed_operations(cache, num_operations: int = 10000) -> float:
    """Benchmark mixed operations (70% GET, 20% PUT, 10% DELETE)."""
    # Pre-populate cache
    for i in range(cache.capacity // 2):
        cache.put(f"key{i}", f"value{i}")
    
    start_time = time.time()
    
    for i in range(num_operations):
        operation = random.random()
        key = f"key{random.randint(0, cache.capacity)}"
        
        if operation < 0.7:  # 70% GET
            cache.get(key)
        elif operation < 0.9:  # 20% PUT
            cache.put(key, f"value{i}")
        else:  # 10% DELETE
            cache.delete(key)
    
    end_time = time.time()
    return end_time - start_time


def benchmark_with_ttl(cache_class, capacity: int = 1000, num_operations: int = 10000) -> float:
    """Benchmark cache with TTL operations."""
    cache = cache_class(capacity=capacity, default_ttl=60)
    
    start_time = time.time()
    
    for i in range(num_operations):
        key = f"key{i}"
        value = f"value{i}"
        ttl = random.randint(10, 120)
        cache.put(key, value, ttl=ttl)
    
    end_time = time.time()
    return end_time - start_time


def benchmark_evictions(cache, num_operations: int = 10000) -> float:
    """Benchmark cache with frequent evictions."""
    start_time = time.time()
    
    # Generate more operations than capacity to force evictions
    for i in range(num_operations):
        key = f"key{i}"
        value = f"value{i}"
        cache.put(key, value)
    
    end_time = time.time()
    return end_time - start_time


def benchmark_hit_rate(cache, num_operations: int = 10000) -> Tuple[float, float]:
    """Benchmark and measure hit rate."""
    # Pre-populate 50% of capacity
    for i in range(cache.capacity // 2):
        cache.put(f"key{i}", f"value{i}")
    
    start_time = time.time()
    
    # 80% of accesses to existing keys, 20% to non-existing
    for i in range(num_operations):
        if random.random() < 0.8:
            key = f"key{random.randint(0, cache.capacity // 2 - 1)}"
        else:
            key = f"key{random.randint(cache.capacity, cache.capacity * 2)}"
        cache.get(key)
    
    end_time = time.time()
    elapsed = end_time - start_time
    
    stats = cache.get_stats()
    hit_rate = stats.hit_rate
    
    return elapsed, hit_rate


def print_results(test_name: str, elapsed: float, operations: int):
    """Print benchmark results."""
    ops_per_sec = operations / elapsed if elapsed > 0 else 0
    avg_time_ms = (elapsed / operations) * 1000 if operations > 0 else 0
    
    print(f"\n{'='*60}")
    print(f"Test: {test_name}")
    print(f"{'='*60}")
    print(f"Total operations: {operations:,}")
    print(f"Total time: {elapsed:.4f} seconds")
    print(f"Operations/sec: {ops_per_sec:,.0f}")
    print(f"Avg time/op: {avg_time_ms:.6f} ms")


def run_all_benchmarks():
    """Run all benchmark tests."""
    setup_logger()
    
    print("\n" + "="*60)
    print("ADVANCED LRU CACHE SYSTEM - PERFORMANCE BENCHMARKS")
    print("="*60)
    
    capacities = [100, 1000, 10000]
    operations = [1000, 10000, 100000]
    
    for capacity in capacities:
        print(f"\n\n{'#'*60}")
        print(f"# CACHE CAPACITY: {capacity}")
        print(f"{'#'*60}")
        
        for num_ops in operations:
            if num_ops > capacity * 100:  # Skip very large tests for small caches
                continue
            
            print(f"\n--- Running with {num_ops:,} operations ---")
            
            # Benchmark LRUCache
            cache = LRUCache(capacity=capacity)
            elapsed = benchmark_put_operations(cache, num_ops)
            print_results(f"LRUCache - PUT operations", elapsed, num_ops)
            
            cache = LRUCache(capacity=capacity)
            elapsed = benchmark_get_operations(cache, num_ops)
            print_results(f"LRUCache - GET operations", elapsed, num_ops)
            
            cache = LRUCache(capacity=capacity)
            elapsed = benchmark_mixed_operations(cache, num_ops)
            print_results(f"LRUCache - Mixed operations", elapsed, num_ops)
            
            # Benchmark ThreadSafeLRUCache
            cache = ThreadSafeLRUCache(capacity=capacity)
            elapsed = benchmark_put_operations(cache, num_ops)
            print_results(f"ThreadSafeLRUCache - PUT operations", elapsed, num_ops)
            
            # Benchmark with evictions
            cache = LRUCache(capacity=capacity)
            elapsed = benchmark_evictions(cache, min(num_ops, capacity * 2))
            print_results(
                f"LRUCache - With evictions",
                elapsed,
                min(num_ops, capacity * 2)
            )
            
            # Benchmark hit rate
            cache = LRUCache(capacity=capacity)
            elapsed, hit_rate = benchmark_hit_rate(cache, num_ops)
            print_results(f"LRUCache - Hit rate test", elapsed, num_ops)
            print(f"Achieved hit rate: {hit_rate:.2f}%")
    
    # Special benchmarks
    print(f"\n\n{'#'*60}")
    print(f"# SPECIAL BENCHMARKS")
    print(f"{'#'*60}")
    
    # TTL operations
    print("\n--- TTL Operations ---")
    elapsed = benchmark_with_ttl(LRUCacheTTL, capacity=1000, num_operations=10000)
    print_results("LRUCacheTTL - PUT with TTL", elapsed, 10000)
    
    print("\n\n" + "="*60)
    print("BENCHMARKS COMPLETED")
    print("="*60)


if __name__ == "__main__":
    run_all_benchmarks()
