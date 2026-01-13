# 🇮🇳 Bharat News Atlas
## Real-Time News Heatmap of India

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Web%20Server-green?style=flat-square&logo=flask)](https://flask.palletsprojects.com/)
[![Leaflet.js](https://img.shields.io/badge/Leaflet.js-Interactive%20Maps-lime?style=flat-square&logo=leaflet)](https://leafletjs.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

**Transform raw news data into stunning geospatial intelligence. Visualize India's news landscape in real-time across all states and major cities.**

[🎯 Features](#features) • [⚡ Quick Start](#quick-start) • [📖 Documentation](#documentation) • [🏗️ Architecture](#architecture)

</div>

---

## 🎯 Features

✨ **Real-Time News Aggregation**
- Pulls from 35+ trusted Indian news sources (TOI, NDTV, India Today, The Hindu, etc.)
- Automatic RSS feed parsing and continuous updates

🗺️ **Interactive Heatmap Visualization**
- Dynamic color-coded markers (yellow → dark red) based on news intensity
- Hover tooltips showing actual news headlines
- Circle marker sizing scales with news volume
- Built with Leaflet.js and OpenStreetMap

🎨 **Smart Geo-Matching**
- Automatically detects state and city mentions in news articles
- Whole-word matching prevents false positives (e.g., "Agra" vs "diagram")
- 28 states + 8 union territories + major cities covered
- Enriched location data with city-level granularity

🚀 **Production-Ready Pipeline**
- Automated 3-step data processing pipeline
- Error handling and graceful failure modes
- Clean separation of concerns (fetch → process → visualize)

📊 **Responsive & Professional UI**
- Full-screen interactive map interface
- Organized legend with color-coded intensity levels
- Mobile-friendly responsive design

---

## ⚡ Quick Start

### Prerequisites
- Python 3.8+
- pip package manager
- Modern web browser

### Installation

```bash
# Clone the repository
git clone https://github.com/indiser/bharat-news-atlas.git
cd bharat-news-atlas

# Install dependencies
pip install -r requirements.txt
```

### Usage

```bash
# Run the complete pipeline
python pipeline.py
```

Then open your browser and navigate to:
```
http://127.0.0.1:5000
```

**That's it!** The application will:
1. 📰 Fetch latest news from 35+ Indian news sources
2. 🔍 Process and geo-match articles to states/cities
3. 🗺️ Display an interactive heatmap with live news data

---

## 📖 Documentation

### Project Structure

```
bharat-news-atlas/
├── 📄 app.py                          # Flask server & API routes
├── 📄 pipeline.py                     # Automated ETL pipeline orchestrator
├── 📄 fetch_news.py                   # RSS feed scraper (35+ sources)
├── 📄 process_data_india.py           # News processing & geo-matching engine
├── 🗂️ templates/
│   └── index.html                     # Interactive Leaflet.js map UI
├── 🗂️ static/                         # CSS, images, favicon
├── 📊 india_locations_cities.csv      # State/city geocoordinates
├── 📊 india_heatmap_data.csv          # Processed output (news counts)
├── 📋 requirements.txt                # Python dependencies
└── 📋 README.md                       # This file
```

### How It Works

#### **Step 1: Fetch News** (`fetch_news.py`)
```python
# Connects to 35+ RSS feeds from Indian news outlets
# Extracts title and description from each article
# Saves to news_data.json
```
- Sources: Times of India, NDTV, India Today, The Hindu, Indian Express, etc.
- Output: `news_data.json` with articles array

#### **Step 2: Process Data** (`process_data_india.py`)
```python
# 1. Loads location data (states + cities with coordinates)
# 2. Searches article text for state/city mentions
# 3. Counts news articles per region
# 4. Generates tooltip content with headlines
```
- Smart matching: Whole-word search prevents false positives
- Includes major cities (Agra, Bangalore, Delhi, Mumbai, etc.)
- Output: `india_heatmap_data.csv` with columns:
  - `State` - State/UT name
  - `Latitude` & `Longitude` - Geo-coordinates
  - `news_count` - Number of mentioning articles
  - `headlines` - Formatted news headlines for tooltips

#### **Step 3: Visualize** (`app.py` + `index.html`)
```python
# Flask API serves geo-tagged news data
# Frontend renders interactive Leaflet.js map
# Real-time updates via color-coded circles
```
- API endpoint: `/api/news` (returns processed heatmap data)
- Color scheme:
  - 🟡 Yellow: 1-3 stories
  - 🟠 Orange: 4-5 stories  
  - 🔴 Red: 6-10 stories
  - 🔻 Dark Red: 11+ stories

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  BHARAT NEWS ATLAS                           │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  📡 DATA INPUT LAYER                                         │
│  ├─ 35+ RSS Feeds → fetch_news.py → news_data.json          │
│  └─ Location Data → india_locations_cities.csv              │
│                                                               │
│  ⚙️ PROCESSING LAYER                                         │
│  ├─ Geo-matching Engine (process_data_india.py)             │
│  └─ Output: india_heatmap_data.csv                          │
│                                                               │
│  🌐 VISUALIZATION LAYER                                      │
│  ├─ Flask Backend (app.py) - /api/news endpoint             │
│  ├─ Leaflet.js Frontend (index.html)                        │
│  └─ Interactive Heatmap UI                                  │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Technologies

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Backend** | Flask | Lightweight web server & API |
| **Data Processing** | Pandas | CSV handling & data transformation |
| **Feed Parsing** | Feedparser | RSS feed extraction |
| **Frontend** | Leaflet.js | Interactive geospatial mapping |
| **Maps** | OpenStreetMap | Base map tiles |
| **Language** | Python 3.8+ | Core logic |

---

## 📋 Requirements

```
Flask           # Web server framework
pandas          # Data processing & CSV handling
feedparser      # RSS/Atom feed parsing
```

See [requirements.txt](requirements.txt) for full dependencies.

---

## 🎨 Customization

### Add More News Sources
Edit `fetch_news.py` and add RSS feed URLs to the `RSS_FEEDS` list:
```python
RSS_FEEDS = [
    "https://your-news-source.com/feed/",
    # ... more feeds
]
```

### Modify Color Thresholds
In `templates/index.html`, update the `getColor()` function:
```javascript
function getColor(d) {
    return d > 10 ? '#800026' : // Dark Red
           d > 5  ? '#BD0026' : // Red
           // ... customize as needed
}
```

### Adjust Geographic Bounds
Update the initial map view in `index.html`:
```javascript
var map = L.map('map').setView([22.3511, 78.6677], 5);
                              // ↑ Latitude, Longitude, Zoom
```

---

## 📊 Sample Output

The interactive map displays:
- **Hover over any circle** → See news headlines for that state
- **Circle size** → Proportional to news volume
- **Circle color** → Indicates intensity (yellow = low, dark red = high)
- **Popup tooltip** → Full state name + exact article count

---

## 🚀 Performance Considerations

- **News Fetching**: ~5-15 seconds (depends on feed responsiveness)
- **Data Processing**: <1 second for 500+ articles
- **Map Load**: <500ms (optimized JSON delivery)
- **Total Pipeline Runtime**: ~30-60 seconds

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| **"news_data.json not found"** | Run `fetch_news.py` first to populate news data |
| **Empty heatmap** | Check that articles contain state/city names; run `process_data_india.py` manually |
| **Slow map loading** | Reduce number of articles or optimize circle rendering |
| **Port 5000 already in use** | Change `app.run(port=5001)` in app.py |

---

## 📈 Future Enhancements

- [ ] Real-time socket updates without page refresh
- [ ] Sentiment analysis (positive/negative/neutral news)
- [ ] Time-series animation showing news trends
- [ ] Export data to JSON/CSV/Excel
- [ ] Mobile app (React Native)
- [ ] News source filtering & custom RSS feeds
- [ ] Caching layer for improved performance
- [ ] Docker containerization

---

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## ✨ Credits

Built with ❤️ using Flask, Pandas, Leaflet.js, and OpenStreetMap.

**Data Sources**: TOI, NDTV, India Today, The Hindu, Indian Express, and 30+ other trusted Indian news outlets.

---

<div align="center">

**[Back to Top](#-bharat-news-atlas)**

Made with 🇮🇳 for India

</div>
