import feedparser
import json
import time

# List of Reliable RSS Feeds (India Specific)
RSS_FEEDS = [
    "https://timesofindia.indiatimes.com/rssfeedstopstories.cms",       # TOI Top Stories
    "https://feeds.feedburner.com/NDTV-LatestNews",
    "https://www.ndtv.com/rss/top-stories",                             # NDTV Top Stories
    "https://www.indiatoday.in/rss/1206584",                            # India Today (National)
    "https://www.indiatoday.in/rss/1206578",
    "https://indianexpress.com/section/india/feed/",                    # Indian Express (India)
    "https://www.thehindu.com/news/national/feeder/default.rss"         # The Hindu (National)
    "https://indianexpress.com/feed/",
    "https://www.firstpost.com/commonfeeds/v1/mfp/rss/web-stories.xml",
    "https://www.business-standard.com/rss/latest.rss",
    "https://www.thetimesofbengal.com/feed/",
    "https://www.headlinesoftoday.com/feed/",
    "https://prod-qt-images.s3.amazonaws.com/production/thequint/feed.xml",
    "https://crowdwisdom.live/feed/",
    "https://newstodaynet.com/feed/",
    "https://www.opindia.com/feed/",
    "https://feeds.indiasnews.net/rss/701ee96610c884a6",
    "https://techgenyz.com/feed/",
    "https://news.abplive.com/home/feed",
    "https://apnlive.com/feed/",
    "https://thenewsmill.com/feed/",
    "https://prod-qt-images.s3.amazonaws.com/production/nationalherald/feed.xml",
    "https://prod-qt-images.s3.amazonaws.com/production/freepressjournal/feed.xml",
    "https://www.india.com/feed/",
    "https://tfipost.com/feed/",
    "https://www.thehindubusinessline.com/?service=rss",
    "https://thebetterindia.com/rss",
    "https://www.siasat.com/feed/",
    "https://www.oneindia.com/rss/news-india-fb.xml",
    "https://organiser.org/feed/",
    "https://news1india.in/feed/",
    "https://timesofindia.indiatimes.com/rssfeedmostrecent.cms",
    "https://timesofindia.indiatimes.com/rssfeeds/-2128936835.cms",
    "https://feeds.feedburner.com/ndtvnews-top-stories",
    "https://feeds.feedburner.com/ndtvnews-latest",
    "https://feeds.feedburner.com/ndtvnews-india-news",
    "https://www.hindustantimes.com/feeds/rss/cities/kolkata-news/rssfeed.xml"
]

articles_list = []

print(f"Connecting to {len(RSS_FEEDS)} news feeds...")

for url in RSS_FEEDS:
    print(f"Fetching: {url}...")
    try:
        feed = feedparser.parse(url)
        
        # Check if feed works
        if feed.bozo:
            print(f"  Warning: Issue parsing {url}")
            continue
            
        print(f"  -> Found {len(feed.entries)} articles.")
        
        for entry in feed.entries:
            # RSS feeds use 'title' and 'summary' (or 'description')
            title = entry.title
            # Clean up the description (sometimes it has HTML tags)
            description = entry.summary if 'summary' in entry else ""
            
            articles_list.append({
                "title": title,
                "description": description
            })
            
    except Exception as e:
        print(f"  Error fetching {url}: {e}")

# Save in the EXACT format your Processor expects
data = {"articles": articles_list}

with open("news_data.json", "w",encoding="utf-8") as filp:
    json.dump(data, filp, indent=4, ensure_ascii=False)

print(f"\nSUCCESS: Saved {len(articles_list)} articles to 'news_data.json'.")