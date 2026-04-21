from flask import Flask, render_template, jsonify, request
import pandas as pd
import os
import asyncio
from sqlalchemy import create_engine
from fetch_news import get_all_news
from process_data_india import process_and_push_to_db
import threading

app = Flask(__name__)

def run_pipeline():
    """Executes the pipeline purely in RAM, no subprocesses, no temp files."""
    print("🚀 Running Background Pipeline natively...")
    try:
        # 1. Fetch data into a RAM variable
        news_data = asyncio.run(get_all_news())
        
        # 2. Pass that variable directly to the database processor
        process_and_push_to_db(news_data)
        
        print("✅ Pipeline execution complete.")
    except Exception as e:
        print(f"❌ Pipeline failed: {e}")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/news')
def get_news():
    try:
        # Pull the secure string
        db_url = os.environ.get("DATABASE_URL")
        if not db_url:
            return jsonify({"error": "Database not configured."}), 500
            
        engine = create_engine(db_url)
        
        # Pull data directly from Neon
        df = pd.read_sql("SELECT * FROM heatmap_data", engine)
        df.fillna("", inplace=True)
        
        news_data = df.to_dict(orient='records')
        return jsonify(news_data)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/trigger-pipeline')
def trigger():
    # 1. Secure the endpoint so random people can't spam your database
    secret = os.environ.get("CRON_SECRET")
    auth_header = request.headers.get("Authorization")
    
    if auth_header != f"Bearer {secret}":
        return jsonify({"error": "Unauthorized. Get out."}), 401
        
    # 2. Run the pipeline in a separate thread so it doesn't block the web response
    threading.Thread(target=run_pipeline).start()
    
    return jsonify({"message": "Pipeline execution triggered successfully."}), 200

if __name__ == '__main__':
    app.run()
