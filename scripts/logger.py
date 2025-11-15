"""
Comprehensive logging system for WeedDB scripts.

Provides structured JSON logging with different levels, rotation, and
performance metrics tracking.

Features:
- Structured JSON logging for easy analysis
- Multiple log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Automatic log rotation (daily)
- Performance metrics tracking
- Context-aware logging with script and operation tracking

Usage:
    from logger import get_logger

    logger = get_logger('add_product.py')
    logger.info('Starting product processing', product_id=12345)
    logger.error('Failed to scrape product', error='Timeout', duration=30.5)
"""

import json
import logging
import logging.handlers
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict

# Constants
LOG_DIR = Path(__file__).parent.parent / "data" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

@dataclass
class LogEntry:
    """Structured log entry"""
    timestamp: str
    level: str
    script: str
    message: str
    operation: Optional[str] = None
    product_id: Optional[int] = None
    product_name: Optional[str] = None
    duration_ms: Optional[float] = None
    success: Optional[bool] = None
    error_type: Optional[str] = None
    error_message: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        # Remove None values for cleaner JSON
        return {k: v for k, v in data.items() if v is not None}

class WeedDBFormatter(logging.Formatter):
    """Custom JSON formatter for WeedDB logs"""

    def format(self, record: logging.LogRecord) -> str:
        # Extract custom fields from record
        log_entry = LogEntry(
            timestamp=datetime.fromtimestamp(record.created).isoformat(),
            level=record.levelname,
            script=getattr(record, 'script', 'unknown'),
            message=record.getMessage(),
            operation=getattr(record, 'operation', None),
            product_id=getattr(record, 'product_id', None),
            product_name=getattr(record, 'product_name', None),
            duration_ms=getattr(record, 'duration_ms', None),
            success=getattr(record, 'success', None),
            error_type=getattr(record, 'error_type', None),
            error_message=getattr(record, 'error_message', None),
            metadata=getattr(record, 'metadata', None)
        )

        return json.dumps(log_entry.to_dict(), ensure_ascii=False)

class WeedDBLogger:
    """Main logger class with convenience methods"""

    def __init__(self, script_name: str):
        self.script_name = script_name
        self.logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        """Setup logger with file and console handlers"""
        logger = logging.getLogger(f'weeddb.{self.script_name}')
        logger.setLevel(logging.DEBUG)

        # Avoid duplicate handlers
        if logger.handlers:
            return logger

        # File handler with rotation
        log_file = LOG_DIR / f"{self.script_name}.log"
        file_handler = logging.handlers.TimedRotatingFileHandler(
            log_file, when='midnight', interval=1, backupCount=30
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(WeedDBFormatter())

        # Console handler for important messages
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(logging.Formatter(
            '%(asctime)s [%(levelname)s] %(script)s: %(message)s',
            datefmt='%H:%M:%S'
        ))

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger

    def _log_with_context(self, level: int, message: str, **kwargs) -> None:
        """Log with additional context fields"""
        # Add script name to all log records
        extra = {'script': self.script_name}
        extra.update(kwargs)

        self.logger.log(level, message, extra=extra)

    def debug(self, message: str, **kwargs) -> None:
        """Log debug message"""
        self._log_with_context(logging.DEBUG, message, **kwargs)

    def info(self, message: str, **kwargs) -> None:
        """Log info message"""
        self._log_with_context(logging.INFO, message, **kwargs)

    def warning(self, message: str, **kwargs) -> None:
        """Log warning message"""
        self._log_with_context(logging.WARNING, message, **kwargs)

    def error(self, message: str, **kwargs) -> None:
        """Log error message"""
        self._log_with_context(logging.ERROR, message, **kwargs)

    def critical(self, message: str, **kwargs) -> None:
        """Log critical message"""
        self._log_with_context(logging.CRITICAL, message, **kwargs)

    def log_operation_start(self, operation: str, **kwargs) -> 'OperationTimer':
        """Start timing an operation and return timer"""
        return OperationTimer(self, operation, **kwargs)

    def log_performance(self, operation: str, duration_ms: float,
                       success: bool = True, **kwargs) -> None:
        """Log performance metrics"""
        level = logging.INFO if success else logging.WARNING
        self._log_with_context(
            level, f"Operation completed: {operation}",
            operation=operation, duration_ms=duration_ms, success=success, **kwargs
        )

class OperationTimer:
    """Context manager for timing operations"""

    def __init__(self, logger: WeedDBLogger, operation: str, **kwargs):
        self.logger = logger
        self.operation = operation
        self.kwargs = kwargs
        self.start_time = None

    def __enter__(self):
        self.start_time = time.time()
        self.logger.debug(f"Starting operation: {self.operation}", **self.kwargs)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.start_time is None:
            return

        duration_ms = (time.time() - self.start_time) * 1000

        if exc_type is not None:
            # Operation failed
            self.logger.error(
                f"Operation failed: {self.operation}",
                operation=self.operation,
                duration_ms=duration_ms,
                success=False,
                error_type=exc_type.__name__,
                error_message=str(exc_val),
                **self.kwargs
            )
        else:
            # Operation succeeded
            self.logger.log_performance(
                self.operation, duration_ms, success=True, **self.kwargs
            )

# Global logger instances cache
_logger_cache: Dict[str, WeedDBLogger] = {}

def get_logger(script_name: str) -> WeedDBLogger:
    """Get or create logger for a script"""
    if script_name not in _logger_cache:
        _logger_cache[script_name] = WeedDBLogger(script_name)
    return _logger_cache[script_name]

def setup_global_logging(level: str = 'INFO') -> None:
    """Setup global logging configuration"""
    # Set level for all weeddb loggers
    level_map = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }

    level_value = level_map.get(level.upper(), logging.INFO)

    # Configure root logger to prevent duplicate messages
    root_logger = logging.getLogger()
    root_logger.setLevel(level_value)

    # Ensure log directory exists
    LOG_DIR.mkdir(parents=True, exist_ok=True)

# Utility functions for log analysis
def get_recent_logs(script_name: str, hours: int = 24) -> list:
    """Get recent log entries for a script"""
    log_file = LOG_DIR / f"{script_name}.log"

    if not log_file.exists():
        return []

    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()[-1000:]  # Last 1000 lines

        logs = []
        cutoff_time = time.time() - (hours * 3600)

        for line in reversed(lines):
            try:
                entry = json.loads(line.strip())
                entry_time = datetime.fromisoformat(entry['timestamp']).timestamp()
                if entry_time >= cutoff_time:
                    logs.append(entry)
                else:
                    break
            except (json.JSONDecodeError, KeyError):
                continue

        return logs[::-1]  # Reverse back to chronological order

    except Exception:
        return []

def get_performance_stats(script_name: str, hours: int = 24) -> Dict[str, Any]:
    """Get performance statistics for a script"""
    logs = get_recent_logs(script_name, hours)

    stats = {
        'total_operations': 0,
        'successful_operations': 0,
        'failed_operations': 0,
        'avg_duration_ms': 0,
        'min_duration_ms': float('inf'),
        'max_duration_ms': 0,
        'error_types': {},
        'operations_by_type': {}
    }

    durations = []

    for entry in logs:
        if 'operation' in entry and 'duration_ms' in entry:
            stats['total_operations'] += 1

            duration = entry['duration_ms']
            durations.append(duration)
            stats['min_duration_ms'] = min(stats['min_duration_ms'], duration)
            stats['max_duration_ms'] = max(stats['max_duration_ms'], duration)

            success = entry.get('success', True)
            if success:
                stats['successful_operations'] += 1
            else:
                stats['failed_operations'] += 1

                error_type = entry.get('error_type', 'unknown')
                stats['error_types'][error_type] = stats['error_types'].get(error_type, 0) + 1

            op_type = entry['operation']
            if op_type not in stats['operations_by_type']:
                stats['operations_by_type'][op_type] = {'count': 0, 'total_duration': 0}
            stats['operations_by_type'][op_type]['count'] += 1
            stats['operations_by_type'][op_type]['total_duration'] += duration

    if durations:
        stats['avg_duration_ms'] = sum(durations) / len(durations)

    if stats['min_duration_ms'] == float('inf'):
        stats['min_duration_ms'] = 0

    return stats

# Backwards compatibility
def log_performance(script_name: str, operation: str, duration_ms: float,
                   success: bool = True, **kwargs) -> None:
    """Legacy function for backwards compatibility"""
    logger = get_logger(script_name)
    logger.log_performance(operation, duration_ms, success, **kwargs)