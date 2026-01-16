# Weather & Kite Flying Checker

A simple web app that lets you check the weather for any location and tells you if it's good weather for flying a kite!

## Features

- 🌤️ Get current weather for any city
- 🪁 Find out if conditions are perfect for kite flying
- 🎨 Beautiful, responsive design with Tailwind CSS
- 🆓 Uses free OpenWeatherMap API

## Kite Flying Criteria

The app determines if it's good kite-flying weather based on:
- **Wind Speed**: Ideal range is 8-24 mph
- **Weather Conditions**: No rain, storms, or thunderstorms
- **Safety**: Warns against flying kites during thunderstorms

## Setup Instructions

### 1. Get a Free API Key

1. Visit [OpenWeatherMap](https://openweathermap.org/api)
2. Click "Sign Up" and create a free account
3. After signing up, go to "API keys" section
4. Copy your API key

### 2. Add Your API Key

1. Open `app.js` in a text editor
2. Find this line: `const API_KEY = 'YOUR_API_KEY_HERE';`
3. Replace `YOUR_API_KEY_HERE` with your actual API key

### 3. Run the App

Simply open `index.html` in your web browser. No build tools or server required!

## Usage

1. Enter a city name (e.g., "London" or "New York, US")
2. Click "Search" or press Enter
3. View the current weather conditions
4. See if it's good weather for flying a kite!

## Technologies Used

- HTML5
- JavaScript (ES6+)
- Tailwind CSS (via CDN)
- OpenWeatherMap API

## License

Free to use and modify!
