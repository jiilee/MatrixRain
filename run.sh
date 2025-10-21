#!/bin/bash
echo "Starting MatrixRain Flask server..."
echo ""
echo "Installing Python dependencies..."
pip3 install -r requirements.txt
echo ""
echo "The Matrix Rain application will be available at: http://localhost:5000"
echo "RSS API available at: http://localhost:5000/api/rss"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""
python3 app.py
