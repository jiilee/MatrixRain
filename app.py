#!/usr/bin/env python3
"""
MatrixRain Flask Backend Server
Serves as RSS proxy to avoid CORS issues
"""

from flask import Flask, jsonify, send_from_directory
import requests
import xml.etree.ElementTree as ET
import json
import os
from datetime import datetime, timedelta
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load RSS feeds from JSON file
def load_rss_feeds():
    """Load RSS feed URLs from JSON file"""
    try:
        with open('rss_feeds.json', 'r') as f:
            data = json.load(f)
            return data.get('feeds', [])
    except FileNotFoundError:
        print("Warning: rss_feeds.json not found")
        return []
    except json.JSONDecodeError:
        print("Error: Invalid JSON in rss_feeds.json")
        return []

def parse_rss_content(xml_text):
    """Parse RSS XML and extract titles and descriptions"""
    try:
        root = ET.fromstring(xml_text)
        items = root.findall('.//item')
        content = []

        for item in items:
            title_elem = item.find('title')
            desc_elem = item.find('description')

            title = title_elem.text.strip() if title_elem is not None and title_elem.text else ''
            description = desc_elem.text.strip() if desc_elem is not None and desc_elem.text else ''

            if title:
                content.append(title.upper())
            if description:
                content.append(description.upper())

        return content
    except ET.ParseError as e:
        print(f"Error parsing RSS XML: {e}")
        return []

@app.route('/api/rss')
def get_rss_content():
    """Fetch and parse RSS feeds, return as JSON"""
    rss_feeds = load_rss_feeds()
    all_content = []

    for feed_url in rss_feeds:
        try:
            print(f"Fetching RSS feed: {feed_url}")
            response = requests.get(feed_url, timeout=10)
            response.raise_for_status()

            content = parse_rss_content(response.text)
            all_content.extend(content)

            print(f"Loaded {len(content)} texts from {feed_url}")

        except requests.RequestException as e:
            print(f"Failed to fetch {feed_url}: {e}")
            continue
        except Exception as e:
            print(f"Error processing {feed_url}: {e}")
            continue

    return jsonify({
        'texts': all_content,
        'count': len(all_content),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/')
def serve_index():
    """Serve the main HTML file"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    return send_from_directory('.', filename)

if __name__ == '__main__':
    print("Starting MatrixRain Flask server...")
    print("RSS API available at: http://localhost:5000/api/rss")
    print("Frontend available at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
