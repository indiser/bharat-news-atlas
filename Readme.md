# # 🇮🇳 Bharat News Atlas

Real-time geospatial visualization of news across India using async RSS aggregation and PostgreSQL.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## Overview

Aggregates news from 39 Indian RSS feeds, matches articles to states/cities using NLP, and renders an interactive Leaflet.js heatmap with color-coded intensity markers.

**Key Features:**
- Async RSS fetching with `aiohttp` (10s timeout per feed)
- PostgreSQL storage via SQLAlchemy (Neon-compatible)
- Automated hourly updates using APScheduler
- Whole-word geo-matching across 36 states/UTs + 500+ cities
- Dynamic circle markers with hover popups

---

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Configure database
echo "DATABASE_URL=postgresql://user:pass@host/db" > .env

# Run server
python app.py
```

Visit `http://localhost:5000`

---

## Architecture

```
┌─────────────────────────────────────────────┐
│  fetch_news.py (Async RSS Aggregator)      │
│  └─ 39 feeds → aiohttp → RAM dict          │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│  process_data_india.py (Geo-Matcher)       │
│  ├─ Loads india_locations_cities.csv       │
│  ├─ Whole-word search in headlines         │
│  └─ Pushes to PostgreSQL (heatmap_data)    │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│  app.py (Flask API + Scheduler)            │
│  ├─ /api/news → JSON from DB               │
│  └─ APScheduler (hourly pipeline)          │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│  templates/index.html (Leaflet.js UI)      │
│  └─ Circle markers + heat layer            │
└─────────────────────────────────────────────┘
```

---

## Project Structure

```
India Heatmap/
├── app.py                      # Flask server + APScheduler
├── fetch_news.py               # Async RSS scraper (39 feeds)
├── process_data_india.py       # Geo-matching + DB writer
├── indian_visualizer.py        # Plotly alternative (unused in web)
├── templates/
│   └── index.html              # Leaflet.js map interface
├── static/
│   └── favicon.png
├── india_locations_cities.csv  # State/city coordinates
├── .env                        # DATABASE_URL config
└── requirements.txt
```

---

## How It Works

### 1. News Fetching (`fetch_news.py`)

Async fetches 39 RSS feeds using `aiohttp`:

```python
async def get_all_news():
    # Returns: {"articles": [{"title": "...", "description": "..."}]}
```

**Sources:** TOI, NDTV, India Today, The Hindu, Indian Express, Business Standard, etc.

### 2. Geo-Processing (`process_data_india.py`)

```python
def process_and_push_to_db(news_data):
    # 1. Load 36 states + cities from CSV
    # 2. Whole-word match: " delhi " in " new delhi summit "
    # 3. Aggregate counts + headlines per region
    # 4. Push to PostgreSQL (replaces table)
```

**Output Schema:**
| Column | Type | Description |
|--------|------|-------------|
| State | TEXT | State/UT name |
| Latitude | FLOAT | Geo-coordinate |
| Longitude | FLOAT | Geo-coordinate |
| news_count | INT | Article mentions |
| headlines | TEXT | HTML-formatted list |

### 3. API Server (`app.py`)

- **`/`** → Renders `index.html`
- **`/api/news`** → Returns JSON from `heatmap_data` table
- **Background Job:** Runs `fetch → process → DB` every hour

### 4. Visualization (`index.html`)

- **Leaflet.js** map centered on India (22.35°N, 78.66°E)
- **Circle Markers:** Size = `news_count * 2`, Color = intensity
- **Heat Layer:** Gradient overlay (yellow → red)
- **Popups:** Hover to see headlines

**Color Scale:**
- 🟡 1-3 stories: `#FEB24C`
- 🟠 4-5 stories: `#FD8D3C`
- 🔴 6-10 stories: `#E31A1C`
- 🔻 11+ stories: `#800026`

---

## Configuration

### Environment Variables

Create `.env` file:

```bash
DATABASE_URL=postgresql://user:password@host:5432/database
```

### RSS Feed Customization

Edit `fetch_news.py`:

```python
RSS_FEEDS = [
    "https://your-feed.com/rss",
    # Add more feeds here
]
```

### Location Data

`india_locations_cities.csv` format:

```csv
Code,Lat,Long,State,cities
DL,28.7041,77.1025,Delhi,"New Delhi, Shahdara, South"
```

---

## Dependencies

```
Flask              # Web framework
pandas             # CSV/data processing
feedparser         # RSS parsing
aiohttp            # Async HTTP client
sqlalchemy         # Database ORM
psycopg2-binary    # PostgreSQL driver
apscheduler        # Background jobs
python-dotenv      # Environment config
gunicorn           # Production WSGI server
```

---

## Deployment

### Local Development

```bash
python app.py  # Runs on port 5000
```

### Production (Gunicorn)

```bash
gunicorn app:app --workers 4 --bind 0.0.0.0:8000
```

### Database Setup

```sql
CREATE TABLE heatmap_data (
    "State" TEXT,
    "Latitude" FLOAT,
    "Longitude" FLOAT,
    news_count INT,
    headlines TEXT
);
```

---

## Performance

- **RSS Fetch:** ~8-12s (parallel async)
- **Geo-Processing:** <2s for 500+ articles
- **DB Write:** <1s (table replace)
- **API Response:** <200ms
- **Total Pipeline:** ~15s

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `DATABASE_URL not found` | Create `.env` file with connection string |
| Empty map | Check DB has data: `SELECT COUNT(*) FROM heatmap_data` |
| Slow fetching | Reduce RSS feeds or increase timeout |
| Port conflict | Change `app.run(port=5001)` |

---

## Alternative Visualizer

`indian_visualizer.py` provides a Plotly-based standalone map:

```bash
python indian_visualizer.py
```

Requires `india_heatmap_data.csv` (legacy CSV-based workflow).

---

## License

MIT License - See [LICENSE](LICENSE) for details.

---

## Credits

Built with Flask, Leaflet.js, OpenStreetMap, and PostgreSQL.

**Data Sources:** 39 Indian news outlets including Times of India, NDTV, The Hindu, Indian Express, and more.
