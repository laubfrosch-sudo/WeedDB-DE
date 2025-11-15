"""
Intelligent caching system for WeedDB scripts.

Provides fast access to frequently requested data with automatic expiration
and memory management.

Features:
- SQLite-based persistent cache
- TTL (Time To Live) support
- LRU-style cleanup for storage limits
- Multiple cache types for different data
- Thread-safe operations

Usage:
    from cache_manager import CacheManager

    cache = CacheManager()
    await cache.set('product_search', 'sourdough', product_data, ttl_hours=24)
    data = await cache.get('product_search', 'sourdough')
"""

import sqlite3
import json
import time
import asyncio
from typing import Any, Optional, Dict, List
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
import hashlib
import logging
from enum import Enum

# Constants
CACHE_DB_PATH = Path(__file__).parent.parent / "data" / "cache.db"
CACHE_DB_PATH.parent.mkdir(parents=True, exist_ok=True)

# Cache entry types
CACHE_PRODUCT_SEARCH = "product_search"    # Product search results
CACHE_PRODUCT_DATA = "product_data"       # Scraped product details
CACHE_PRICE_DATA = "price_data"          # Price information
CACHE_URL_MAPPING = "url_mapping"        # URL to product ID mappings
CACHE_SEARCH_RESULTS = "search_results"   # General search results

@dataclass
class CacheEntry:
    """Cache entry structure"""
    key: str
    data: Any
    entry_type: str
    created_at: float
    expires_at: Optional[float]
    access_count: int = 0
    last_accessed: Optional[float] = None

    def is_expired(self) -> bool:
        """Check if entry is expired"""
        if self.expires_at is None:
            return False
        return time.time() > self.expires_at

    def to_db_row(self) -> tuple:
        """Convert to database row format"""
        return (
            self.key,
            json.dumps(self.data, ensure_ascii=False),
            self.entry_type,
            self.created_at,
            self.expires_at,
            self.access_count,
            self.last_accessed
        )

    @classmethod
    def from_db_row(cls, row: tuple) -> 'CacheEntry':
        """Create from database row"""
        key, data_json, entry_type, created_at, expires_at, access_count, last_accessed = row
        data = json.loads(data_json)
        return cls(key, data, entry_type, created_at, expires_at, access_count, last_accessed)

class CacheManager:
    """Main cache management class"""

    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or CACHE_DB_PATH
        self.logger = logging.getLogger(__name__)
        self._init_db()

    def _init_db(self):
        """Initialize cache database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS cache (
                    key TEXT NOT NULL,
                    data TEXT NOT NULL,
                    entry_type TEXT NOT NULL,
                    created_at REAL NOT NULL,
                    expires_at REAL,
                    access_count INTEGER DEFAULT 0,
                    last_accessed REAL,
                    PRIMARY KEY (key, entry_type)
                )
            ''')

            # Create indexes for performance
            conn.execute('CREATE INDEX IF NOT EXISTS idx_expires_at ON cache(expires_at)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_entry_type ON cache(entry_type)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_last_accessed ON cache(last_accessed)')

    def _get_connection(self) -> sqlite3.Connection:
        """Get database connection"""
        return sqlite3.connect(self.db_path)

    async def get(self, entry_type: str, key: str) -> Optional[Any]:
        """Get cached data"""
        def _query():
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT key, data, entry_type, created_at, expires_at, access_count, last_accessed
                    FROM cache
                    WHERE key = ? AND entry_type = ?
                ''', (key, entry_type))

                row = cursor.fetchone()
                if not row:
                    return None

                entry = CacheEntry.from_db_row(row)

                # Check if expired
                if entry.is_expired():
                    # Delete expired entry
                    cursor.execute(
                        'DELETE FROM cache WHERE key = ? AND entry_type = ?',
                        (key, entry_type)
                    )
                    conn.commit()
                    return None

                # Update access statistics
                now = time.time()
                cursor.execute('''
                    UPDATE cache
                    SET access_count = access_count + 1, last_accessed = ?
                    WHERE key = ? AND entry_type = ?
                ''', (now, key, entry_type))
                conn.commit()

                return entry.data

        # Run in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, _query)

    async def set(self, entry_type: str, key: str, data: Any,
                 ttl_seconds: Optional[float] = None) -> None:
        """Set cached data"""
        now = time.time()
        expires_at = now + ttl_seconds if ttl_seconds else None

        entry = CacheEntry(key, data, entry_type, now, expires_at)

        def _insert():
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO cache
                    (key, data, entry_type, created_at, expires_at, access_count, last_accessed)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', entry.to_db_row())
                conn.commit()

        # Run in thread pool
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, _insert)

        self.logger.debug(f"Cached {entry_type}:{key} (TTL: {ttl_seconds}s)")

    async def delete(self, entry_type: str, key: str) -> bool:
        """Delete cached entry"""
        def _delete():
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'DELETE FROM cache WHERE key = ? AND entry_type = ?',
                    (key, entry_type)
                )
                conn.commit()
                return cursor.rowcount > 0

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, _delete)

    async def clear_expired(self) -> int:
        """Clear all expired entries"""
        def _clear():
            with self._get_connection() as conn:
                cursor = conn.cursor()
                now = time.time()
                cursor.execute('DELETE FROM cache WHERE expires_at < ?', (now,))
                deleted_count = cursor.rowcount
                conn.commit()
                return deleted_count

        loop = asyncio.get_event_loop()
        deleted = await loop.run_in_executor(None, _clear)

        if deleted > 0:
            self.logger.info(f"Cleared {deleted} expired cache entries")

        return deleted

    async def clear_type(self, entry_type: str) -> int:
        """Clear all entries of a specific type"""
        def _clear():
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM cache WHERE entry_type = ?', (entry_type,))
                deleted_count = cursor.rowcount
                conn.commit()
                return deleted_count

        loop = asyncio.get_event_loop()
        deleted = await loop.run_in_executor(None, _clear)

        if deleted > 0:
            self.logger.info(f"Cleared {deleted} cache entries of type {entry_type}")

        return deleted

    async def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        def _stats():
            with self._get_connection() as conn:
                cursor = conn.cursor()

                # Total entries
                cursor.execute('SELECT COUNT(*) FROM cache')
                total_entries = cursor.fetchone()[0]

                # Entries by type
                cursor.execute('''
                    SELECT entry_type, COUNT(*), AVG(access_count), MAX(last_accessed)
                    FROM cache
                    GROUP BY entry_type
                ''')
                type_stats = {}
                for row in cursor.fetchall():
                    entry_type, count, avg_access, last_access = row
                    type_stats[entry_type] = {
                        'count': count,
                        'avg_access_count': avg_access or 0,
                        'last_accessed': last_access
                    }

                # Expired entries
                now = time.time()
                cursor.execute('SELECT COUNT(*) FROM cache WHERE expires_at < ?', (now,))
                expired_count = cursor.fetchone()[0]

                return {
                    'total_entries': total_entries,
                    'expired_entries': expired_count,
                    'type_stats': type_stats,
                    'db_size_mb': self.db_path.stat().st_size / (1024 * 1024) if self.db_path.exists() else 0
                }

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, _stats)

    async def cleanup_lru(self, max_entries: int = 1000) -> int:
        """Remove least recently used entries to stay under max_entries limit"""
        def _cleanup():
            with self._get_connection() as conn:
                cursor = conn.cursor()

                # Count current entries
                cursor.execute('SELECT COUNT(*) FROM cache')
                current_count = cursor.fetchone()[0]

                if current_count <= max_entries:
                    return 0

                # Delete oldest accessed entries
                to_delete = current_count - max_entries
                cursor.execute('''
                    DELETE FROM cache
                    WHERE key IN (
                        SELECT key FROM cache
                        ORDER BY last_accessed ASC, created_at ASC
                        LIMIT ?
                    )
                ''', (to_delete,))
                deleted_count = cursor.rowcount
                conn.commit()
                return deleted_count

        loop = asyncio.get_event_loop()
        deleted = await loop.run_in_executor(None, _cleanup)

        if deleted > 0:
            self.logger.info(f"Cleaned up {deleted} LRU cache entries")

        return deleted

# Convenience functions
async def get_cached_product_search(search_term: str) -> Optional[Any]:
    """Get cached product search results"""
    cache = CacheManager()
    return await cache.get(CACHE_PRODUCT_SEARCH, search_term)

async def set_cached_product_search(search_term: str, data: Any, ttl_hours: float = 24) -> None:
    """Cache product search results"""
    cache = CacheManager()
    await cache.set(CACHE_PRODUCT_SEARCH, search_term, data, ttl_hours * 3600)

async def get_cached_product_data(product_id: int) -> Optional[Any]:
    """Get cached product data"""
    cache = CacheManager()
    return await cache.get(CACHE_PRODUCT_DATA, str(product_id))

async def set_cached_product_data(product_id: int, data: Any, ttl_hours: float = 1) -> None:
    """Cache product data"""
    cache = CacheManager()
    await cache.set(CACHE_PRODUCT_DATA, str(product_id), data, ttl_hours * 3600)

# Global cache manager instance
_default_cache = None

def get_cache_manager() -> CacheManager:
    """Get default cache manager instance"""
    global _default_cache
    if _default_cache is None:
        _default_cache = CacheManager()
    return _default_cache