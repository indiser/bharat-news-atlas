from flask import Flask, render_template, jsonify, request
import pandas as pd
import os
from sqlalchemy import create_engine

app = Flask(__name__)

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
    

if __name__ == '__main__':
    app.run()
