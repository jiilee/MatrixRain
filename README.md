# MatrixRain
Classic Matrix-style falling characters animation

## Description
A mesmerizing recreation of the iconic "Matrix" digital rain effect using HTML5 Canvas and JavaScript. Watch as green characters cascade down the screen, creating the signature look from the famous movie franchise.

## Features
- **Authentic Matrix Effect**: Falling green characters with glow effects
- **Mixed Character Sets**: Combines Japanese Katakana and Latin alphanumeric characters
- **RSS Feed Integration**: Dynamically incorporates real-time content from news and tech RSS feeds in deep red
- **Visual Distinction**: RSS content appears in deep red with extended fade-out effect for better readability
- **Interactive**: Click anywhere to reset and randomize the falling patterns
- **Responsive Design**: Automatically adapts to window size changes
- **Performance Optimized**: Smooth 60fps animation with efficient rendering
- **Customizable**: Easy to modify colors, speed, character sets, and RSS feed sources

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/jiilee/MatrixRain.git
   ```

2. **Install Python dependencies** (Flask and RSS processing libraries)

3. **For Windows users**: Double-click `run.bat` to install dependencies and start the server

4. **For Linux/Mac users**: Run `./run.sh` in terminal to install dependencies and start the server

## Quick Start
- **Windows**: Double-click `run.bat`
- **Linux/Mac**: Run `./run.sh` in terminal
- **Browser**: Go to `http://localhost:5000`

## Server Architecture
The application uses a **Flask backend server** with intelligent caching for optimal performance:

- **Frontend**: HTML5 Canvas application with Matrix rain animation
- **Backend**: Flask server that fetches RSS feeds server-side and serves them as JSON
- **RSS Feeds**: 100+ RSS feeds from news, technology, sports, and lifestyle sources
- **In-Memory Caching**: RSS content cached for 5 minutes for instant UI refreshes
- **No CORS Issues**: All RSS fetching happens server-side, eliminating browser CORS restrictions

### API Endpoints
- **`GET /api/rss`** - Get RSS content (uses caching for performance)
- **`GET /api/cache/status`** - Check cache status and age
- **`GET /api/cache/clear`** - Clear RSS cache (for debugging)

## Usage
Simply open `index.html` in any modern web browser. The animation will start automatically.

### Controls
- **Click**: Reset all falling characters to create new random patterns

### Customization
The animation can be easily customized by modifying the JavaScript variables in `index.html`:
- `fontSize`: Size of the falling characters (default: 14)
- `matrixChars`: Character set used for the rain effect
- Animation speed can be adjusted in the `setInterval(draw, 50)` line

### RSS Feed Integration
The application automatically loads content from various news and technology RSS feeds, mixing real-world content with traditional Matrix characters:

**Included RSS Feeds:**
- CNN News
- BBC News
- The New York Times
- Reuters
- TechCrunch
- The Verge
- Wired
- Ars Technica
- Reddit Technology
- Reddit World News

**How it Works:**
- RSS content is fetched asynchronously when the page loads
- Complete article titles and descriptions are extracted from RSS feeds
- Specific columns (every 8th column) are designated as RSS feed columns
- Each RSS column displays one complete text (title or description) as individual characters
- **RSS characters appear in deep red** with an extended fade-out effect for better visibility
- Characters from the RSS text fall vertically, one at a time, maintaining the Matrix rain effect
- When reaching the end of the text, it automatically restarts from the beginning
- Other columns continue to display traditional Matrix characters in bright green (Japanese Katakana and Latin alphanumeric)
- If RSS feeds fail to load, the animation falls back to traditional Matrix characters only

**Visual Design:**
- **Traditional Matrix columns**: Bright green characters with random opacity
- **RSS columns**: Deep red characters with gradual fade-out effect over the last 200px
- **Enhanced readability**: RSS content stays visible longer as it falls

**Adding Custom Feeds:**
To add your own RSS feeds, modify the `rssFeeds` array in the JavaScript code:
```javascript
let rssFeeds = [
    'https://your-custom-feed.xml',
    // ... add more feeds
];
```

## Technical Details
- **Technology**: Pure HTML5 Canvas and vanilla JavaScript
- **No Dependencies**: Runs entirely in the browser with no external libraries
- **File Size**: Minimal footprint for fast loading
- **Browser Support**: Works in all modern browsers that support Canvas

## Project Structure
```
MatrixRain/
├── index.html      # Main HTML file with embedded CSS and JavaScript
├── app.py          # Flask backend server (RSS proxy)
├── requirements.txt # Python dependencies for Flask server
├── rss_feeds.json  # RSS feed URLs configuration
├── README.md       # This file
├── octos.json      # Project configuration
├── run.bat         # Windows launcher (installs deps + starts Flask)
├── run.sh          # Unix/Linux launcher (installs deps + starts Flask)
├── AGENTS.md       # Safety documentation
├── CLAUDE.md       # Safety documentation
└── CLINE.md        # Safety documentation
```

## License
This project is open source and available under the [MIT License](LICENSE).
