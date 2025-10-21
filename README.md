# MatrixRain
Classic Matrix-style falling characters animation

## Description
A mesmerizing recreation of the iconic "Matrix" digital rain effect using HTML5 Canvas and JavaScript. Watch as green characters cascade down the screen, creating the signature look from the famous movie franchise.

## Features
- **Authentic Matrix Effect**: Falling green characters with glow effects
- **Mixed Character Sets**: Combines Japanese Katakana and Latin alphanumeric characters
- **Interactive**: Click anywhere to reset and randomize the falling patterns
- **Responsive Design**: Automatically adapts to window size changes
- **Performance Optimized**: Smooth 60fps animation with efficient rendering
- **Customizable**: Easy to modify colors, speed, and character sets

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/jiilee/MatrixRain.git
   ```

2. Open `index.html` in your web browser or serve it using a local server:
   ```bash
   # Using Python (if installed)
   python -m http.server 8000

   # Using Node.js (if installed)
   npx serve .
   ```

## Usage
Simply open `index.html` in any modern web browser. The animation will start automatically.

### Controls
- **Click**: Reset all falling characters to create new random patterns

### Customization
The animation can be easily customized by modifying the JavaScript variables in `index.html`:
- `fontSize`: Size of the falling characters (default: 14)
- `matrixChars`: Character set used for the rain effect
- Animation speed can be adjusted in the `setInterval(draw, 50)` line

## Technical Details
- **Technology**: Pure HTML5 Canvas and vanilla JavaScript
- **No Dependencies**: Runs entirely in the browser with no external libraries
- **File Size**: Minimal footprint for fast loading
- **Browser Support**: Works in all modern browsers that support Canvas

## Project Structure
```
MatrixRain/
├── index.html      # Main HTML file with embedded CSS and JavaScript
├── README.md       # This file
└── octos.json      # Project configuration
```

## License
This project is open source and available under the [MIT License](LICENSE).
