from flask import Flask, render_template, jsonify
import pandas as pd
import os
import subprocess
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

app = Flask(__name__)

def run_pipeline():
    """Executes the fetch and process scripts autonomously."""
    print("🚀 Running Background Pipeline...")
    try:
        subprocess.run(["python", "fetch_news.py"], check=True)
        subprocess.run(["python", "process_data_india.py"], check=True)
        print("✅ Data successfully updated.")
    except Exception as e:
        print(f"❌ Pipeline failed: {e}")

scheduler = BackgroundScheduler()
scheduler.add_job(
    func=run_pipeline, 
    trigger="interval", 
    hours=1,
    next_run_time=datetime.now()
)
scheduler.start()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/news')
def get_news():
    try:
        # Load your processed data
        if os.path.exists("india_heatmap_data.csv"):
            df = pd.read_csv("india_heatmap_data.csv")
            df = df.fillna("")
            news_data = df.to_dict(orient='records')
            return jsonify(news_data)
        else:
            return jsonify([])
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run()
