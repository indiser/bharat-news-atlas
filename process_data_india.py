import pandas as pd
import json
import os

# 1. Load the Location Data (which now has the 'cities' column)
# Try absolute path first, then relative
file_path = "C:/Users/ranab/OneDrive/Desktop/India Heatmap/india_locations_cities.csv"
if not os.path.exists(file_path):
    file_path = "india_locations_cities.csv"

try:
    # We load the file you just created, which has State, Lat, Long, and Cities
    df_locations = pd.read_csv(file_path)
except FileNotFoundError:
    print(f"Error: Could not find 'india_locations_cities.csv' at {file_path}")
    exit()

# 2. Load News Data
try:
    with open("news_data.json", "r", encoding="utf-8") as file:
        data = json.load(file)
except FileNotFoundError:
    print("Error: news_data.json not found. Run your fetch script first.")
    exit()

articles = data.get('articles', [])
print(f"Loaded {len(articles)} articles. Processing...")

# 3. Build Search Blob
processed_articles = []
for article in articles:
    t = article['title'] if article['title'] else ""
    d = article['description'] if article['description'] else ""
    # We search inside both Title and Description
    searchable = f"{t} {d}".lower()
    display = t.strip()
    if display:
        processed_articles.append((searchable, display))

# 4. The "City-Only" Matcher Logic
def get_state_stats(row):
    # 1. Start with the State Name
    state_name = str(row['State']).lower()
    valid_names = [state_name]
    
    # 2. Add Cities from the CSV column
    # The column 'cities' is a string like "Agra, Noida, Varanasi"
    cities_str = str(row['cities']) 
    
    if cities_str and cities_str != "nan":
        # Split by comma, strip whitespace, and convert to lowercase
        city_list = [c.strip().lower() for c in cities_str.split(',')]
        # Filter out empty strings just in case
        valid_names.extend([c for c in city_list if c])
        
    found_headlines = []
    
    # 3. Search Logic
    for search_text, display_headline in processed_articles:
        for term in valid_names:
            # "Pad" the term to match whole words only
            # e.g., prevents "agra" matching inside "diagram"
            if f" {term} " in f" {search_text} ":
                if display_headline not in found_headlines:
                    found_headlines.append(display_headline)
                break 
    
    count = len(found_headlines)
    
    if count > 0:
        # Join ALL headlines with <br> tags for the tooltip
        hover_text = "<br>".join([f"➤ {h}" for h in found_headlines])
    else:
        hover_text = "No active news."
    
    return pd.Series([count, hover_text])

print("Scanning headlines against States & Cities...")
# Applying to your new dataframe structure
df_locations[['news_count', 'headlines']] = df_locations.apply(get_state_stats, axis=1)

# 5. Filter and Save
# Remove states with 0 news to keep the map clean
df_final = df_locations[df_locations['news_count'] > 0].copy()

# Sort by news count
df_final.sort_values(by='news_count', ascending=False, inplace=True)

df_final.drop("cities",axis=1,inplace=True)

# We save it as 'india_heatmap_data.csv' because that is what your Visualizer expects
df_final.to_csv("india_heatmap_data.csv", index=False)
print(f"DONE. Saved {len(df_final)} active regions using City aliases.")