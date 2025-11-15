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
async def get_products(limit: int = 50, offset: int = 0, search: Optional[str] = None):
    """Get products with optional search"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
            SELECT p.id, p.name, p.thc_percent, p.cbd_percent, p.genetics,
                   pr.name as producer, p.rating, p.review_count
            FROM products p
            LEFT JOIN producers pr ON p.producer_id = pr.id
        """

        params = []
        if search:
            query += " WHERE p.name LIKE ?"
            params.append(f"%{search}%")

        query += " ORDER BY p.name LIMIT ? OFFSET ?"
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
        return {"products": products, "limit": limit, "offset": offset}

    except Exception as e:
        logger.error(f"Products error: {e}") if logger else print(f"Products error: {e}")
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
            "top_expensive": df.nlargest(5, 'price_per_g')[['name', 'price_per_g', 'pharmacy']].to_dict('records'),
            "top_cheap": df.nsmallest(5, 'price_per_g')[['name', 'price_per_g', 'pharmacy']].to_dict('records')
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