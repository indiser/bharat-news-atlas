from flask import Flask, render_template, jsonify
import pandas as pd
import os

app = Flask(__name__)

# 1. The Home Page
@app.route('/')
def home():
    return render_template('index.html')

# 2. The Data API (Frontend calls this to get points)
@app.route('/api/news')
def get_news():
    try:
        # Load your processed data
        if os.path.exists("india_heatmap_data.csv"):
            df = pd.read_csv("india_heatmap_data.csv")
            
            # Fill NaNs to avoid JSON errors
            df = df.fillna("")
            
            # Convert to a list of dictionaries (JSON friendly)
            news_data = df.to_dict(orient='records')
            return jsonify(news_data)
        else:
            return jsonify([])
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    print("Starting Flask Server...")
    print("Go to: http://127.0.0.1:5000")

    app.run()
