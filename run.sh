#!/bin/bash
echo "Starting MatrixRain server..."
echo ""
echo "The Matrix Rain application will be available at: http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""
python3 -m http.server 8000
