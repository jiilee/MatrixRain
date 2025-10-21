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

# In-memory cache for RSS content
rss_cache = {
    'data': None,
    'timestamp': None,
    'count': 0
}

# Cache TTL in seconds (5 minutes)
CACHE_TTL = 300

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

def is_cache_valid():
    """Check if cached RSS data is still valid"""
    if rss_cache['data'] is None or rss_cache['timestamp'] is None:
        return False

    cache_age = datetime.now() - rss_cache['timestamp']
    return cache_age.total_seconds() < CACHE_TTL

def get_cached_rss_content():
    """Return cached RSS content if valid"""
    if is_cache_valid():
        print(f"📋 Using cached RSS data ({rss_cache['count']} texts, {CACHE_TTL}s TTL)")
        return {
            'texts': rss_cache['data'],
            'count': rss_cache['count'],
            'timestamp': rss_cache['timestamp'].isoformat(),
            'cached': True
        }
    return None

def update_rss_cache(texts):
    """Update the RSS cache with new data"""
    rss_cache['data'] = texts
    rss_cache['timestamp'] = datetime.now()
    rss_cache['count'] = len(texts)
    print(f"💾 Updated RSS cache with {len(texts)} texts")

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
    """Fetch and parse RSS feeds with caching, return as JSON"""

    # Check cache first
    cached_data = get_cached_rss_content()
    if cached_data:
        return jsonify(cached_data)

    # Cache miss - fetch fresh data
    print("🔄 Cache miss - fetching fresh RSS data...")
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

    # Update cache with fresh data
    if all_content:
        update_rss_cache(all_content)

    return jsonify({
        'texts': all_content,
        'count': len(all_content),
        'timestamp': datetime.now().isoformat(),
        'cached': False
    })

@app.route('/api/cache/status')
def get_cache_status():
    """Get cache status information"""
    if rss_cache['timestamp']:
        cache_age = datetime.now() - rss_cache['timestamp']
        age_seconds = int(cache_age.total_seconds())
        remaining_ttl = max(0, CACHE_TTL - age_seconds)

        return jsonify({
            'cached': is_cache_valid(),
            'count': rss_cache['count'],
            'timestamp': rss_cache['timestamp'].isoformat(),
            'age_seconds': age_seconds,
            'ttl_seconds': CACHE_TTL,
            'remaining_ttl': remaining_ttl
        })
    else:
        return jsonify({
            'cached': False,
            'count': 0,
            'timestamp': None,
            'age_seconds': None,
            'ttl_seconds': CACHE_TTL,
            'remaining_ttl': 0
        })

@app.route('/api/cache/clear')
def clear_cache():
    """Clear RSS cache (for debugging)"""
    rss_cache['data'] = None
    rss_cache['timestamp'] = None
    rss_cache['count'] = 0
    print("🗑️  RSS cache cleared")

    return jsonify({
        'status': 'cache_cleared',
        'message': 'RSS cache has been cleared'
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
    print("🚀 Starting MatrixRain Flask server...")
    print("📋 RSS API available at: http://localhost:5000/api/rss")
    print("🔍 Cache status API: http://localhost:5000/api/cache/status")
    print("🗑️  Cache clear API: http://localhost:5000/api/cache/clear")
    print("🌐 Frontend available at: http://localhost:5000")
    print(f"💾 RSS cache TTL: {CACHE_TTL} seconds ({CACHE_TTL//60} minutes)")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)
