import os
import sys
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
from datetime import datetime, timezone
load_dotenv()

def process_and_push_to_db(news_data):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    locations_path = os.path.join(BASE_DIR, "india_locations_cities.csv")

    if not os.path.exists(locations_path):
        print(f"❌ Error: Could not find '{locations_path}'.")
        return

    try:
        df_locations = pd.read_csv(locations_path)
    except Exception as e:
        print(f"❌ Error reading locations CSV: {e}")
        return

    # ACCEPT DATA FROM RAM DIRECTLY
    articles = news_data.get('articles', [])
    print(f"Loaded {len(articles)} articles into memory. Processing...")

    processed_articles = []
    for article in articles:
        t = article['title'] if article['title'] else ""
        d = article['description'] if article['description'] else ""
        searchable = f"{t} {d}".lower()
        display = t.strip()
        if display:
            processed_articles.append((searchable, display))

    def get_state_stats(row):
        state_name = str(row['State']).lower()
        valid_names = [state_name]
        cities_str = str(row['cities']) 
        if cities_str and cities_str != "nan":
            city_list = [c.strip().lower() for c in cities_str.split(',')]
            valid_names.extend([c for c in city_list if c])
            
        found_headlines = []
        for search_text, display_headline in processed_articles:
            for term in valid_names:
                if f" {term} " in f" {search_text} ":
                    if display_headline not in found_headlines:
                        found_headlines.append(display_headline)
                    break 
        
        count = len(found_headlines)
        hover_text = "<br>".join([f"➤ {h}" for h in found_headlines]) if count > 0 else "No active news."
        return pd.Series([count, hover_text])

    print("Scanning headlines against States & Cities...")
    df_locations[['news_count', 'headlines']] = df_locations.apply(get_state_stats, axis=1)

    df_final = df_locations[df_locations['news_count'] > 0].copy()
    df_final.sort_values(by='news_count', ascending=False, inplace=True)

    if "cities" in df_final.columns:
        df_final.drop("cities", axis=1, inplace=True)
    
    df_final['last_updated'] = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        print("❌ CRITICAL: DATABASE_URL environment variable is missing.")
        return

    try:
        print("Connecting to Neon Database...")
        engine = create_engine(db_url)
        df_final.to_sql("heatmap_data", engine, if_exists="replace", index=False)
        print(f"✅ DONE. Successfully pushed {len(df_final)} active regions to Neon.")
    except Exception as e:
        print(f"❌ Database Error: {e}")



# import os
# import sys
# import pandas as pd
# from sqlalchemy import create_engine
# from dotenv import load_dotenv
# import json

# # 1. Load the local .env file
# load_dotenv()

# # 2. Anchor ALL files strictly to the script's directory
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# locations_path = os.path.join(BASE_DIR, "india_locations_cities.csv")
# news_path = os.path.join(BASE_DIR, "news_data.json") # Ensure fetch_news.py saves it as this

# # 3. Load Locations (Loud Failure)
# if not os.path.exists(locations_path):
#     print(f"❌ Error: Could not find '{locations_path}'.")
#     sys.exit(1)

# try:
#     df_locations = pd.read_csv(locations_path)
# except Exception as e:
#     print(f"❌ Error reading locations CSV: {e}")
#     sys.exit(1)

# # 4. Load News Data (Loud Failure)
# try:
#     with open(news_path, "r", encoding="utf-8") as file:
#         data = json.load(file)
# except FileNotFoundError:
#     print(f"❌ Error: {news_path} not found. Run your fetch script first.")
#     sys.exit(1)
# except Exception as e:
#     print(f"❌ Error reading news JSON: {e}")
#     sys.exit(1)

# articles = data.get('articles', [])
# print(f"Loaded {len(articles)} articles. Processing...")

# # 5. Build Search Blob
# processed_articles = []
# for article in articles:
#     t = article['title'] if article['title'] else ""
#     d = article['description'] if article['description'] else ""
#     searchable = f"{t} {d}".lower()
#     display = t.strip()
#     if display:
#         processed_articles.append((searchable, display))

# # 6. The "City-Only" Matcher Logic
# def get_state_stats(row):
#     state_name = str(row['State']).lower()
#     valid_names = [state_name]
    
#     cities_str = str(row['cities']) 
#     if cities_str and cities_str != "nan":
#         city_list = [c.strip().lower() for c in cities_str.split(',')]
#         valid_names.extend([c for c in city_list if c])
        
#     found_headlines = []
#     for search_text, display_headline in processed_articles:
#         for term in valid_names:
#             if f" {term} " in f" {search_text} ":
#                 if display_headline not in found_headlines:
#                     found_headlines.append(display_headline)
#                 break 
    
#     count = len(found_headlines)
#     if count > 0:
#         hover_text = "<br>".join([f"➤ {h}" for h in found_headlines])
#     else:
#         hover_text = "No active news."
    
#     return pd.Series([count, hover_text])

# print("Scanning headlines against States & Cities...")
# df_locations[['news_count', 'headlines']] = df_locations.apply(get_state_stats, axis=1)

# df_final = df_locations[df_locations['news_count'] > 0].copy()
# df_final.sort_values(by='news_count', ascending=False, inplace=True)

# # 7. Strip dead weight before pushing to DB
# if "cities" in df_final.columns:
#     df_final.drop("cities", axis=1, inplace=True)

# # 8. Push to Neon
# db_url = os.environ.get("DATABASE_URL")
# if not db_url:
#     print("❌ CRITICAL: DATABASE_URL environment variable is missing.")
#     sys.exit(1)

# try:
#     print("Connecting to Neon Database...")
#     engine = create_engine(db_url)
#     df_final.to_sql("heatmap_data", engine, if_exists="replace", index=False)
#     print(f"✅ DONE. Successfully pushed {len(df_final)} active regions to Neon.")
# except Exception as e:
#     print(f"❌ Database Error: {e}")
#     sys.exit(1)
