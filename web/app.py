"""
WeedDB Web Interface - FastAPI Application

Provides a modern web interface for WeedDB with:
- Live dashboard with metrics and charts
- Product management and search
- Batch operations via web interface
- Analytics and price trend visualizations
- REST API for external integrations

Usage:
    # Development
    uvicorn web.app:app --reload --host 0.0.0.0 --port 8000

    # Production
    uvicorn web.app:app --host 0.0.0.0 --port 8000 --workers 4
"""

import asyncio
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any, Optional
import json

from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.utils import PlotlyJSONEncoder

# Import our existing modules
try:
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

    from logger import get_logger
    from error_handler import get_error_handler, RetryConfig
    from cache_manager import get_cache_manager
    import sqlite3
    import subprocess

    logger = get_logger('web_app')
    error_handler = get_error_handler()
    cache = get_cache_manager()
except ImportError as e:
    print(f"Warning: Could not import modules: {e}")
    logger = None
    error_handler = None
    cache = None

# Configuration
PROJECT_ROOT = Path(__file__).parent.parent
DATABASE_PATH = PROJECT_ROOT / "data" / "WeedDB.db"
TEMPLATES_DIR = PROJECT_ROOT / "web" / "templates"
STATIC_DIR = PROJECT_ROOT / "web" / "static"

# FastAPI app
app = FastAPI(
    title="WeedDB Web Interface",
    description="Modern web interface for cannabis product price tracking",
    version="0.1.2-alpha",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Mount static files
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Templates
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# Database connection helper
def get_db_connection():
    """Get database connection"""
    return sqlite3.connect(DATABASE_PATH)

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Main dashboard page"""
    try:
        # Get basic stats
        stats = await get_system_stats()

        return templates.TemplateResponse(
            "dashboard.html",
            {
                "request": request,
                "stats": stats,
                "title": "WeedDB Dashboard"
            }
        )
    except Exception as e:
        logger.error(f"Dashboard error: {e}") if logger else print(f"Dashboard error: {e}")
        raise HTTPException(status_code=500, detail="Dashboard error")

@app.get("/api/stats")
async def get_system_stats():
    """Get system statistics"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Basic product stats
        cursor.execute("SELECT COUNT(*) FROM products")
        product_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM producers")
        producer_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM pharmacies")
        pharmacy_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM prices")
        price_count = cursor.fetchone()[0]

        # Recent prices
        cursor.execute("""
            SELECT COUNT(*) FROM prices
            WHERE timestamp > datetime('now', '-24 hours')
        """)
        recent_prices = cursor.fetchone()[0]

        # Latest update
        cursor.execute("SELECT MAX(timestamp) FROM prices")
        latest_update = cursor.fetchone()[0]

        conn.close()

        return {
            "products": product_count,
            "producers": producer_count,
            "pharmacies": pharmacy_count,
            "total_prices": price_count,
            "recent_prices": recent_prices,
            "latest_update": latest_update,
            "database_size_mb": round(DATABASE_PATH.stat().st_size / (1024 * 1024), 2) if DATABASE_PATH.exists() else 0
        }

    except Exception as e:
        logger.error(f"Stats error: {e}") if logger else print(f"Stats error: {e}")
        return {"error": str(e)}

@app.get("/api/products")
async def get_products(
    limit: int = 50,
    offset: int = 0,
    search: Optional[str] = None,
    genetics: Optional[str] = None,
    producer: Optional[str] = None,
    min_rating: Optional[float] = None,
    sort_by: str = "name",
    sort_order: str = "asc"
):
    """Get products with advanced filtering, sorting and pagination"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Build query with filters
        query = """
            SELECT p.id, p.name, p.thc_percent, p.cbd_percent, p.genetics,
                   pr.name as producer, p.rating, p.review_count
            FROM products p
            LEFT JOIN producers pr ON p.producer_id = pr.id
            WHERE 1=1
        """

        params = []

        # Apply filters
        if search:
            query += " AND p.name LIKE ?"
            params.append(f"%{search}%")

        if genetics:
            query += " AND p.genetics = ?"
            params.append(genetics)

        if producer:
            query += " AND pr.name LIKE ?"
            params.append(f"%{producer}%")

        if min_rating is not None:
            query += " AND p.rating >= ?"
            params.append(min_rating)

        # Validate sort parameters
        allowed_sort_fields = {
            "name": "p.name",
            "rating": "p.rating",
            "thc_percent": "p.thc_percent",
            "review_count": "p.review_count"
        }

        if sort_by not in allowed_sort_fields:
            sort_by = "name"

        sort_column = allowed_sort_fields[sort_by]
        sort_direction = "DESC" if sort_order.lower() == "desc" else "ASC"

        query += f" ORDER BY {sort_column} {sort_direction}"

        # Get total count for pagination info
        count_query = query.replace("SELECT p.id, p.name, p.thc_percent, p.cbd_percent, p.genetics,\n                   pr.name as producer, p.rating, p.review_count\n            FROM products p\n            LEFT JOIN producers pr ON p.producer_id = pr.id\n            WHERE 1=1", "SELECT COUNT(*) FROM products p LEFT JOIN producers pr ON p.producer_id = pr.id WHERE 1=1")
        count_query = count_query.split(" ORDER BY")[0]  # Remove ORDER BY for count

        cursor.execute(count_query, params)
        total_count = cursor.fetchone()[0]

        # Add pagination
        query += " LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        cursor.execute(query, params)
        products = []

        for row in cursor.fetchall():
            products.append({
                "id": row[0],
                "name": row[1],
                "thc_percent": row[2],
                "cbd_percent": row[3],
                "genetics": row[4],
                "producer": row[5],
                "rating": row[6],
                "review_count": row[7]
            })

        conn.close()

        return {
            "products": products,
            "pagination": {
                "total": total_count,
                "limit": limit,
                "offset": offset,
                "has_more": offset + limit < total_count
            },
            "filters": {
                "search": search,
                "genetics": genetics,
                "producer": producer,
                "min_rating": min_rating
            },
            "sorting": {
                "sort_by": sort_by,
                "sort_order": sort_order
            }
        }

    except Exception as e:
        logger.error(f"Products error: {e}") if logger else print(f"Products error: {e}")
        raise HTTPException(status_code=500, detail="Database error")

@app.get("/api/products/{product_id}")
async def get_product_detail(product_id: int):
    """Get detailed information about a specific product"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Get product details
        cursor.execute("""
            SELECT p.id, p.name, p.variant, p.thc_percent, p.cbd_percent, p.genetics,
                   pr.name as producer, p.rating, p.review_count, p.stock_level,
                   p.irradiation, p.country, p.effects, p.complaints, p.url, p.last_updated
            FROM products p
            LEFT JOIN producers pr ON p.producer_id = pr.id
            WHERE p.id = ?
        """, (product_id,))

        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Product not found")

        product = {
            "id": row[0],
            "name": row[1],
            "variant": row[2],
            "thc_percent": row[3],
            "cbd_percent": row[4],
            "genetics": row[5],
            "producer": row[6],
            "rating": row[7],
            "review_count": row[8],
            "stock_level": row[9],
            "irradiation": row[10],
            "country": row[11],
            "effects": row[12],
            "complaints": row[13],
            "url": row[14],
            "last_updated": row[15]
        }

        # Get price history
        cursor.execute("""
            SELECT price_per_g, category, timestamp, pharmacy_id, ph.name as pharmacy_name
            FROM prices pr
            JOIN pharmacies ph ON pr.pharmacy_id = ph.id
            WHERE pr.product_id = ?
            ORDER BY timestamp DESC
            LIMIT 20
        """, (product_id,))

        price_history = []
        for price_row in cursor.fetchall():
            price_history.append({
                "price_per_g": price_row[0],
                "category": price_row[1],
                "timestamp": price_row[2],
                "pharmacy_id": price_row[3],
                "pharmacy_name": price_row[4]
            })

        # Get current prices
        cursor.execute("""
            SELECT pr.price_per_g, pr.category, ph.name as pharmacy_name
            FROM prices pr
            JOIN pharmacies ph ON pr.pharmacy_id = ph.id
            WHERE pr.product_id = ? AND pr.timestamp = (
                SELECT MAX(timestamp) FROM prices WHERE product_id = ? AND category = pr.category
            )
        """, (product_id, product_id))

        current_prices = {}
        for price_row in cursor.fetchall():
            current_prices[price_row[1]] = {
                "price_per_g": price_row[0],
                "pharmacy": price_row[2]
            }

        conn.close()

        return {
            "product": product,
            "current_prices": current_prices,
            "price_history": price_history
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Product detail error: {e}") if logger else print(f"Product detail error: {e}")
        raise HTTPException(status_code=500, detail="Database error")

@app.get("/api/analytics/prices")
async def get_price_analytics():
    """Get price analytics and trends"""
    try:
        conn = get_db_connection()

        # Get price statistics
        df = pd.read_sql_query("""
            SELECT p.name, pr.price_per_g, pr.category, pr.timestamp,
                   ph.name as pharmacy
            FROM prices pr
            JOIN products p ON pr.product_id = p.id
            JOIN pharmacies ph ON pr.pharmacy_id = ph.id
            ORDER BY pr.timestamp DESC
            LIMIT 1000
        """, conn)

        conn.close()

        if df.empty:
            return {"error": "No price data available"}

        # Basic analytics
        analytics = {
            "total_records": len(df),
            "avg_price_top": round(df[df['category'] == 'top']['price_per_g'].mean(), 2),
            "avg_price_all": round(df[df['category'] == 'all']['price_per_g'].mean(), 2),
            "price_range": {
                "min": round(df['price_per_g'].min(), 2),
                "max": round(df['price_per_g'].max(), 2)
            },
            "top_expensive": df.nlargest(5, 'price_per_g')[['name', 'price_per_g', 'pharmacy']].values.tolist(),
            "top_cheap": df.nsmallest(5, 'price_per_g')[['name', 'price_per_g', 'pharmacy']].values.tolist()
        }

        return analytics

    except Exception as e:
        logger.error(f"Analytics error: {e}") if logger else print(f"Analytics error: {e}")
        raise HTTPException(status_code=500, detail="Analytics error")

@app.post("/api/batch/update")
async def trigger_batch_update(background_tasks: BackgroundTasks):
    """Trigger a batch price update"""
    try:
        # Add background task
        background_tasks.add_task(run_batch_update)

        return {"message": "Batch update started in background", "status": "running"}

    except Exception as e:
        logger.error(f"Batch trigger error: {e}") if logger else print(f"Batch trigger error: {e}")
        raise HTTPException(status_code=500, detail="Batch trigger failed")

# Global storage for batch status updates
batch_status_updates = []

@app.post("/api/batch/status")
async def receive_batch_status(status_data: Dict[str, Any]):
    """Receive status updates from batch processing scripts"""
    try:
        # Add timestamp if not present
        if 'timestamp' not in status_data:
            status_data['timestamp'] = datetime.now().isoformat()

        # Store status update (keep last 100 entries)
        batch_status_updates.append(status_data)
        if len(batch_status_updates) > 100:
            batch_status_updates.pop(0)

        logger.info(f"Received batch status update for: {status_data.get('product_name', 'unknown')}") if logger else None

        return {"status": "received", "message": "Status update stored"}

    except Exception as e:
        logger.error(f"Status update error: {e}") if logger else print(f"Status update error: {e}")
        raise HTTPException(status_code=500, detail="Status update failed")

@app.get("/api/batch/status")
async def get_batch_status(limit: int = 20):
    """Get recent batch processing status updates"""
    try:
        # Return most recent status updates
        recent_updates = batch_status_updates[-limit:] if batch_status_updates else []

        return {
            "status_updates": recent_updates,
            "total_updates": len(batch_status_updates),
            "returned_count": len(recent_updates)
        }

    except Exception as e:
        logger.error(f"Get status error: {e}") if logger else print(f"Get status error: {e}")
        raise HTTPException(status_code=500, detail="Status retrieval failed")

async def run_batch_update():
    """Run batch update in background"""
    try:
        if logger:
            logger.info("Starting background batch update")

        # Run the update script
        scripts_dir = PROJECT_ROOT / "scripts"
        result = subprocess.run(
            [sys.executable, str(scripts_dir / "update_prices.py")],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT,
            timeout=600  # 10 minutes
        )

        if logger:
            if result.returncode == 0:
                logger.info("Background batch update completed successfully")
            else:
                logger.error(f"Background batch update failed: {result.stderr}")

    except subprocess.TimeoutExpired:
        if logger:
            logger.error("Background batch update timed out")
    except Exception as e:
        if logger:
            logger.error(f"Background batch update error: {e}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        conn.close()

        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "database": "connected",
            "version": "0.1.2-alpha"
        }

    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

if __name__ == "__main__":
    # Development server
    uvicorn.run(
        "web.app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )