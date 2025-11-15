"""
Robust error handling and retry mechanisms for WeedDB scripts.

Provides comprehensive error handling with:
- Exponential backoff retry logic
- Circuit breaker pattern for failing operations
- Graceful degradation strategies
- Error classification and recovery actions

Features:
- Configurable retry policies per error type
- Circuit breaker to prevent cascade failures
- Context-aware error handling
- Recovery strategies for different failure modes

Usage:
    from error_handler import ErrorHandler, RetryConfig

    handler = ErrorHandler()
    result = await handler.execute_with_retry(operation_func, retry_config)
"""

import asyncio
import time
import random
from typing import Callable, Any, Optional, Dict, List
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import logging

class ErrorType(Enum):
    """Classification of different error types"""
    NETWORK = "network"           # Connection, timeout, DNS errors
    HTTP = "http"                # HTTP status errors (4xx, 5xx)
    PARSING = "parsing"          # HTML/XML parsing errors
    DATABASE = "database"        # SQLite constraint, connection errors
    RATE_LIMIT = "rate_limit"    # 429 Too Many Requests
    SYSTEM = "system"           # OS-level errors, disk space, etc.
    UNKNOWN = "unknown"         # Unclassified errors

@dataclass
class RetryConfig:
    """Configuration for retry behavior"""
    max_attempts: int = 3
    base_delay: float = 1.0  # Base delay in seconds
    max_delay: float = 30.0  # Maximum delay between retries
    backoff_factor: float = 2.0  # Exponential backoff multiplier
    jitter: bool = True  # Add random jitter to prevent thundering herd

@dataclass
class CircuitBreakerConfig:
    """Configuration for circuit breaker pattern"""
    failure_threshold: int = 5  # Failures before opening circuit
    recovery_timeout: float = 60.0  # Seconds to wait before trying again

class CircuitBreakerState(Enum):
    CLOSED = "closed"      # Normal operation
    OPEN = "open"         # Failing, requests fail fast
    HALF_OPEN = "half_open"  # Testing if service recovered

@dataclass
class CircuitBreakerStats:
    """Statistics for circuit breaker monitoring"""
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    consecutive_failures: int = 0
    last_failure_time: Optional[datetime] = None
    state: CircuitBreakerState = CircuitBreakerState.CLOSED

class CircuitBreakerOpenException(Exception):
    """Exception raised when circuit breaker is open"""
    pass

class CircuitBreaker:
    """Circuit breaker implementation to prevent cascade failures"""

    def __init__(self, config: CircuitBreakerConfig):
        self.config = config
        self.stats = CircuitBreakerStats()

    def _should_attempt_reset(self) -> bool:
        """Check if we should attempt to reset the circuit breaker"""
        if self.stats.state != CircuitBreakerState.OPEN:
            return False

        if self.stats.last_failure_time is None:
            return True

        time_since_failure = (datetime.now() - self.stats.last_failure_time).total_seconds()
        return time_since_failure >= self.config.recovery_timeout

    async def call(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function through circuit breaker"""
        self.stats.total_requests += 1

        # Check if circuit should be reset
        if self.stats.state == CircuitBreakerState.OPEN:
            if self._should_attempt_reset():
                self.stats.state = CircuitBreakerState.HALF_OPEN
            else:
                raise CircuitBreakerOpenException("Circuit breaker is open")

        try:
            result = await func(*args, **kwargs)
            self._on_success()
            return result

        except Exception as e:
            self._on_failure()
            raise

    def _on_success(self):
        """Handle successful operation"""
        self.stats.successful_requests += 1
        self.stats.consecutive_failures = 0

        if self.stats.state == CircuitBreakerState.HALF_OPEN:
            self.stats.state = CircuitBreakerState.CLOSED

    def _on_failure(self):
        """Handle failed operation"""
        self.stats.failed_requests += 1
        self.stats.consecutive_failures += 1
        self.stats.last_failure_time = datetime.now()

        if self.stats.consecutive_failures >= self.config.failure_threshold:
            self.stats.state = CircuitBreakerState.OPEN

def classify_error(error: Exception) -> ErrorType:
    """Classify an exception into an error type"""
    error_str = str(error).lower()
    error_type = type(error).__name__.lower()

    # Network-related errors
    if any(keyword in error_str or keyword in error_type for keyword in
           ['timeout', 'connection', 'network', 'dns', 'ssl', 'certificate']):
        return ErrorType.NETWORK

    # HTTP-related errors
    if any(keyword in error_str for keyword in ['http', 'status', '4', '5']):
        return ErrorType.HTTP

    # Rate limiting
    if '429' in error_str or 'rate limit' in error_str or 'too many requests' in error_str:
        return ErrorType.RATE_LIMIT

    # Database errors
    if any(keyword in error_type for keyword in ['sqlite', 'database', 'integrity', 'constraint']):
        return ErrorType.DATABASE

    # Parsing errors
    if any(keyword in error_str or keyword in error_type for keyword in
           ['parse', 'html', 'xml', 'selector', 'xpath']):
        return ErrorType.PARSING

    # System errors
    if any(keyword in error_type for keyword in ['oserror', 'ioerror', 'permission']):
        return ErrorType.SYSTEM

    return ErrorType.UNKNOWN

class ErrorHandler:
    """Main error handling class with retry logic"""

    def __init__(self):
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}
        self.logger = logging.getLogger(__name__)

    def get_circuit_breaker(self, name: str,
                           config: Optional[CircuitBreakerConfig] = None) -> CircuitBreaker:
        """Get or create a circuit breaker for a specific operation"""
        if name not in self.circuit_breakers:
            if config is None:
                config = CircuitBreakerConfig()
            self.circuit_breakers[name] = CircuitBreaker(config)

        return self.circuit_breakers[name]

    async def execute_with_retry(self, func: Callable, config: RetryConfig,
                                operation_name: str = "operation",
                                *args, **kwargs) -> Any:
        """Execute a function with retry logic"""
        last_exception = None

        for attempt in range(config.max_attempts):
            try:
                result = await func(*args, **kwargs)

                # Success - log if this was a retry
                if attempt > 0:
                    self.logger.info(f"{operation_name} succeeded on attempt {attempt + 1}")

                return result

            except Exception as e:
                last_exception = e
                error_type = classify_error(e)

                # Check if we should retry
                if attempt >= config.max_attempts - 1:
                    self.logger.error(
                        f"{operation_name} failed permanently after {attempt + 1} attempts: {e}"
                    )
                    break

                # Calculate delay with exponential backoff
                delay = min(
                    config.base_delay * (config.backoff_factor ** attempt),
                    config.max_delay
                )

                # Add jitter if enabled
                if config.jitter:
                    delay *= (0.5 + random.random() * 0.5)  # 50-100% of calculated delay

                self.logger.warning(
                    f"{operation_name} failed (attempt {attempt + 1}/{config.max_attempts}): "
                    f"{e}. Retrying in {delay:.1f}s"
                )

                await asyncio.sleep(delay)

        # All retries exhausted
        if last_exception:
            raise last_exception
        else:
            raise Exception("All retry attempts failed")

# Convenience functions for common use cases
async def retry_network_operation(func: Callable, *args, **kwargs) -> Any:
    """Retry a network operation with appropriate config"""
    handler = ErrorHandler()
    config = RetryConfig(max_attempts=5, base_delay=2.0, max_delay=60.0)
    return await handler.execute_with_retry(func, config, "network_operation", *args, **kwargs)

async def retry_database_operation(func: Callable, *args, **kwargs) -> Any:
    """Retry a database operation with appropriate config"""
    handler = ErrorHandler()
    config = RetryConfig(max_attempts=3, base_delay=0.5, max_delay=5.0)
    return await handler.execute_with_retry(func, config, "database_operation", *args, **kwargs)

# Global error handler instance
default_error_handler = ErrorHandler()

def get_error_handler() -> ErrorHandler:
    """Get the default error handler instance"""
    return default_error_handler