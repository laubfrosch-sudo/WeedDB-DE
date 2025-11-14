#!/usr/bin/env python3
"""
Smart retry mechanism with exponential backoff for network failures.

This module provides retry functionality for network operations
with configurable backoff strategies and error handling.
"""

import asyncio
import random
import time
from typing import Any, Callable, Optional, Type, Union
from functools import wraps


class RetryError(Exception):
    """Custom exception for retry failures"""
    pass


def retry_with_backoff(
    max_attempts: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    backoff_factor: float = 2.0,
    jitter: bool = True,
    exceptions: tuple = (Exception,),
    on_retry: Optional[Callable[[Exception, int], None]] = None
) -> Callable:
    """
    Decorator for retrying functions with exponential backoff.
    
    Args:
        max_attempts: Maximum number of retry attempts
        base_delay: Initial delay between retries in seconds
        max_delay: Maximum delay between retries in seconds
        backoff_factor: Multiplier for exponential backoff
        jitter: Whether to add random jitter to prevent thundering herd
        exceptions: Tuple of exception types to catch and retry on
        on_retry: Optional callback called on each retry attempt
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def async_wrapper(*args, **kwargs) -> Any:
            last_exception = None
            
            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    
                    if attempt == max_attempts - 1:
                        # Final attempt failed, re-raise
                        raise RetryError(f"Failed after {max_attempts} attempts") from e
                    
                    # Calculate delay for next attempt
                    delay = min(base_delay * (backoff_factor ** attempt), max_delay)
                    
                    # Add jitter to prevent thundering herd
                    if jitter:
                        delay = delay * (0.5 + random.random() * 0.5)
                    
                    if on_retry:
                        on_retry(e, attempt + 1)
                    
                    print(f"   🔄 Retry {attempt + 1}/{max_attempts} after {delay:.2f}s: {str(e)[:100]}")
                    await asyncio.sleep(delay)
            
            # This should never be reached, but just in case
            raise RetryError("Unexpected error in retry mechanism") from last_exception
        
        def sync_wrapper(*args, **kwargs) -> Any:
            last_exception = None
            
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    
                    if attempt == max_attempts - 1:
                        # Final attempt failed, re-raise
                        raise RetryError(f"Failed after {max_attempts} attempts") from e
                    
                    # Calculate delay for next attempt
                    delay = min(base_delay * (backoff_factor ** attempt), max_delay)
                    
                    # Add jitter to prevent thundering herd
                    if jitter:
                        delay = delay * (0.5 + random.random() * 0.5)
                    
                    if on_retry:
                        on_retry(e, attempt + 1)
                    
                    print(f"   🔄 Retry {attempt + 1}/{max_attempts} after {delay:.2f}s: {str(e)[:100]}")
                    time.sleep(delay)
            
            # This should never be reached, but just in case
            raise RetryError("Unexpected error in retry mechanism") from last_exception
        
        # Return appropriate wrapper based on whether function is async
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator


# Example usage and default configurations
NETWORK_RETRY_CONFIG = {
    'fast': {
        'max_attempts': 3,
        'base_delay': 0.5,
        'max_delay': 5.0,
        'backoff_factor': 2.0,
        'jitter': True
    },
    'standard': {
        'max_attempts': 5,
        'base_delay': 1.0,
        'max_delay': 30.0,
        'backoff_factor': 2.0,
        'jitter': True
    },
    'conservative': {
        'max_attempts': 7,
        'base_delay': 2.0,
        'max_delay': 60.0,
        'backoff_factor': 2.5,
        'jitter': True
    }
}


def get_retry_config(name: str = 'standard') -> dict:
    """Get a predefined retry configuration"""
    return NETWORK_RETRY_CONFIG.get(name, NETWORK_RETRY_CONFIG['standard'])


# Convenience decorators for common use cases
@retry_with_backoff(**NETWORK_RETRY_CONFIG['fast'])
def fast_retry(func: Callable) -> Callable:
    """Fast retry decorator for quick operations"""
    return func


@retry_with_backoff(**NETWORK_RETRY_CONFIG['standard'])
def standard_retry(func: Callable) -> Callable:
    """Standard retry decorator for most operations"""
    return func


@retry_with_backoff(**NETWORK_RETRY_CONFIG['conservative'])
def conservative_retry(func: Callable) -> Callable:
    """Conservative retry decorator for critical operations"""
    return func


if __name__ == '__main__':
    # Example usage
    @standard_retry
    def example_function():
        import random
        if random.random() < 0.7:  # 70% chance of failure
            raise ConnectionError("Simulated network error")
        return "Success!"
    
    try:
        result = example_function()
        print(f"Result: {result}")
    except RetryError as e:
        print(f"Failed: {e}")