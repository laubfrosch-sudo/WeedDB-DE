# 🌐 Web Interface Guide (v0.1.2)

**GitHub Repository:** [https://github.com/laubfrosch-sudo/WeedDB-DE](https://github.com/laubfrosch-sudo/WeedDB-DE)

This guide explains how to use WeedDB's modern web interface to explore, analyze, and manage cannabis product data.

## 🚀 Quick Start

### 1. Start Web Interface

```bash
# Ensure all dependencies are installed
pip install -r requirements.txt

# Change to web directory
cd web

# Start development server
python3 -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### 2. Access

**Dashboard:** http://localhost:8000
**API Documentation:** http://localhost:8000/docs

## 📊 Using the Dashboard

### Live Metrics

The dashboard shows current statistics from your WeedDB:

- **📦 Products:** Number of cannabis strains in database
- **🏭 Producers:** Number of different manufacturers
- **🏥 Pharmacies:** Number of shipping pharmacies
- **💰 Prices:** Number of stored price records

### Quick Actions

- **🔄 Update Prices:** Starts batch update of all product prices
- **📄 Generate Overview:** Creates new SORTEN_ÜBERSICHT.md
- **📋 View Logs:** Shows system logs

### Auto-Refresh

Dashboard updates automatically every 30 seconds with latest data.

## 🔍 Exploring Products

### Search Products

```bash
# Get all products (first 50)
curl "http://localhost:8000/api/products"

# Search for specific strains
curl "http://localhost:8000/api/products?search=sour"

# Filter by genetics
curl "http://localhost:8000/api/products?genetics=indica"

# Filter by producer
curl "http://localhost:8000/api/products?producer=pedanios"

# Set minimum rating
curl "http://localhost:8000/api/products?min_rating=4.0"

# Change sorting
curl "http://localhost:8000/api/products?sort_by=rating&sort_order=desc"

# Combined filters
curl "http://localhost:8000/api/products?search=diesel&genetics=indica&min_rating=4.0&limit=10"
```

### Get Product Details

```bash
# Detailed information about a product
curl "http://localhost:8000/api/products/808"

# Example response:
{
  "product": {
    "id": 808,
    "name": "White Widow",
    "variant": null,
    "thc_percent": 18.0,
    "cbd_percent": 1.0,
    "genetics": "Indica",
    "producer": "Weeco",
    "rating": 4.2,
    "review_count": 1250,
    "stock_level": 100,
    "irradiation": "No",
    "country": "Netherlands",
    "effects": "Relaxing, pain-relieving",
    "complaints": "Sleep disorders, chronic pain",
    "url": "https://shop.dransay.com/product/...",
    "last_updated": "2025-11-15T..."
  },
  "current_prices": {
    "top": {"price_per_g": 6.50, "pharmacy": "Pharmacy A"},
    "all": {"price_per_g": 6.20, "pharmacy": "Pharmacy B"}
  },
  "price_history": [
    {
      "price_per_g": 6.50,
      "category": "top",
      "timestamp": "2025-11-15T...",
      "pharmacy_name": "Pharmacy A"
    }
  ]
}
```

### Product Details

Each product includes:
- **ID:** Unique identifier
- **Name:** Product name (e.g. "Sourdough")
- **THC/CBD:** Cannabinoid content in percent
- **Genetics:** Indica, Sativa, Hybrid, etc.
- **Producer:** Manufacturer name
- **Rating:** User rating (1-5 stars)
- **Reviews:** Number of reviews

## 📈 Price Analytics

### Current Price Statistics

```bash
curl http://localhost:8000/api/analytics/prices
```

**Includes:**
- Total number of price records
- Average prices (Top pharmacies vs. All)
- Price range (Minimum/Maximum)
- Top 5 most expensive products
- Top 5 cheapest products

### Price Trends

API provides historical price data for trend analysis and market monitoring.

## 🔧 Batch Operations

### Update Prices

```bash
# Via web interface (recommended)
# Click "Update Prices" button in dashboard

# Or via API
curl -X POST http://localhost:8000/api/batch/update
```

**What happens:**
- All product prices updated from shop.dransay.com
- New price records stored in history
- Dashboard shows live update status

### Generate Overview

```bash
# Via web interface
# Click "Generate Overview" button in dashboard

# Or manually
python3 scripts/generate_overview.py
```

**Creates:** `docs/SORTEN_ÜBERSICHT.md` with current data

## 📚 API Documentation

### Swagger UI

Visit http://localhost:8000/docs for interactive API documentation:

- **All endpoints** listed
- **Parameters** and **response schemas** explained
- **Test interface** directly in browser
- **Example requests** and responses

### ReDoc

Alternative documentation: http://localhost:8000/redoc

## 🔧 Advanced Features

### System Monitoring

```bash
# Health check
curl http://localhost:8000/health

# Detailed system information
curl http://localhost:8000/api/stats
```

### Database Status

- **Connection status:** Database reachable?
- **Last update:** When was data last updated?
- **Storage:** Database size
- **Performance metrics:** Response times

## 🐛 Troubleshooting

### Server won't start

```bash
# Check dependencies
python3 -c "import fastapi, uvicorn; print('OK')"

# Check port conflicts
lsof -i :8000

# Start with debug output
python3 -m uvicorn web.app:app --log-level debug
```

### API returns errors

```bash
# Test health check
curl http://localhost:8000/health

# Check database connection
python3 -c "import sqlite3; conn = sqlite3.connect('data/WeedDB.db'); print('DB OK'); conn.close()"
```

### Slow performance

- **Optimize database:** Run `VACUUM` and `ANALYZE`
- **Clear cache:** Remove temporary files
- **Restart server:** With more workers for production

## 🚀 Production Deployment

### Multiple Workers (Recommended)

```bash
# 4 workers for better performance
python3 -m uvicorn web.app:app --host 0.0.0.0 --port 8000 --workers 4
```

### Background Service

```bash
# With systemd (Linux)
# Or with launchd (macOS)
# Or with screen/tmux
```

### Reverse Proxy (SSL)

```bash
# nginx or Caddy for SSL termination
# Example nginx config:
server {
    listen 443 ssl;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 📊 Understanding Data

### Product Categories

- **Indica:** Relaxing, calming
- **Sativa:** Energetic, focusing
- **Hybrid:** Mix of both
- **THC/CBD:** Active ingredient content in percent

### Price Differences

- **Top Pharmacies:** Curated selection of trusted pharmacies
- **All Pharmacies:** Complete market overview
- **Historical Data:** Price development over time

## 🎯 Best Practices

### Regular Maintenance

1. **Daily price updates** for current data
2. **Weekly overview** generation
3. **Monthly backups** and optimizations

### Performance Optimization

1. **Use cache** for repeated queries
2. **Batch updates** instead of individual requests
3. **Respect API limits** (don't overload)

### Data Security

1. **Regular database backups**
2. **Rotate logs** (don't let them grow infinitely)
3. **API access** only through trusted networks

## 📞 Support

### Common Issues

**Q: Dashboard won't load?**
A: Make sure server is running (`ps aux | grep uvicorn`)

**Q: API returns errors?**
A: Check database connection and logs

**Q: Prices are outdated?**
A: Run batch update or start cron job

### Finding Logs

```bash
# Server logs in terminal
# Additional logs: tail -f data/logs/web_app.log
# System logs: tail -f data/logs/*.log
```

---

## 🎉 Summary

The WeedDB Web Interface provides you with:

- **📊 Live Dashboard** with current metrics
- **🔍 Product Search** and filtering
- **📈 Price Analytics** and trends
- **🚀 Batch Operations** for mass updates
- **📚 Complete API** with documentation
- **🔧 System Monitoring** and health checks

**Start now:** http://localhost:8000

**API Documentation:** http://localhost:8000/docs

**Enjoy exploring your cannabis data! 🌿📊**