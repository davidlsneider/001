// OpenWeatherMap API Configuration
// Get your free API key at: https://openweathermap.org/api
const API_KEY = 'YOUR_API_KEY_HERE'; // Replace with your actual API key
const API_URL = 'https://api.openweathermap.org/data/2.5/weather';

// DOM Elements
const cityInput = document.getElementById('cityInput');
const searchBtn = document.getElementById('searchBtn');
const errorDiv = document.getElementById('error');
const loadingDiv = document.getElementById('loading');
const resultsDiv = document.getElementById('results');

// Weather Display Elements
const cityNameEl = document.getElementById('cityName');
const weatherIconEl = document.getElementById('weatherIcon');
const temperatureEl = document.getElementById('temperature');
const descriptionEl = document.getElementById('description');
const windSpeedEl = document.getElementById('windSpeed');
const humidityEl = document.getElementById('humidity');
const feelsLikeEl = document.getElementById('feelsLike');

// Kite Flying Elements
const kiteResultDiv = document.getElementById('kiteResult');
const kiteIconEl = document.getElementById('kiteIcon');
const kiteAnswerEl = document.getElementById('kiteAnswer');
const kiteReasonEl = document.getElementById('kiteReason');

// Event Listeners
searchBtn.addEventListener('click', handleSearch);
cityInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        handleSearch();
    }
});

async function handleSearch() {
    const city = cityInput.value.trim();

    if (!city) {
        showError('Please enter a city name');
        return;
    }

    if (API_KEY === 'YOUR_API_KEY_HERE') {
        showError('Please add your OpenWeatherMap API key in app.js');
        return;
    }

    hideError();
    hideResults();
    showLoading();

    try {
        const weatherData = await fetchWeather(city);
        displayWeather(weatherData);
        displayKiteFlyingResult(weatherData);
        showResults();
    } catch (error) {
        showError(error.message);
    } finally {
        hideLoading();
    }
}

async function fetchWeather(city) {
    const url = `${API_URL}?q=${encodeURIComponent(city)}&appid=${API_KEY}&units=imperial`;

    const response = await fetch(url);

    if (!response.ok) {
        if (response.status === 404) {
            throw new Error('City not found. Please check the spelling and try again.');
        } else if (response.status === 401) {
            throw new Error('Invalid API key. Please check your OpenWeatherMap API key.');
        } else {
            throw new Error('Failed to fetch weather data. Please try again later.');
        }
    }

    return await response.json();
}

function displayWeather(data) {
    cityNameEl.textContent = `${data.name}, ${data.sys.country}`;

    const iconCode = data.weather[0].icon;
    weatherIconEl.src = `https://openweathermap.org/img/wn/${iconCode}@2x.png`;
    weatherIconEl.alt = data.weather[0].description;

    temperatureEl.textContent = `${Math.round(data.main.temp)}°F`;
    descriptionEl.textContent = capitalize(data.weather[0].description);
    windSpeedEl.textContent = `${Math.round(data.wind.speed)} mph`;
    humidityEl.textContent = `${data.main.humidity}%`;
    feelsLikeEl.textContent = `${Math.round(data.main.feels_like)}°F`;
}

function displayKiteFlyingResult(data) {
    const result = checkKiteFlyingConditions(data);

    if (result.goodForKites) {
        kiteResultDiv.className = 'bg-gradient-to-br from-green-100 to-green-200 rounded-lg p-6 text-center';
        kiteIconEl.textContent = '🪁';
        kiteAnswerEl.textContent = 'YES! Great for flying a kite!';
        kiteAnswerEl.className = 'text-2xl font-bold mb-2 text-green-800';
        kiteReasonEl.className = 'text-sm text-green-700';
    } else {
        kiteResultDiv.className = 'bg-gradient-to-br from-red-100 to-red-200 rounded-lg p-6 text-center';
        kiteIconEl.textContent = '❌';
        kiteAnswerEl.textContent = 'NO, not ideal for kites';
        kiteAnswerEl.className = 'text-2xl font-bold mb-2 text-red-800';
        kiteReasonEl.className = 'text-sm text-red-700';
    }

    kiteReasonEl.textContent = result.reason;
}

function checkKiteFlyingConditions(data) {
    const windSpeed = data.wind.speed; // mph
    const weatherMain = data.weather[0].main.toLowerCase();
    const weatherDescription = data.weather[0].description.toLowerCase();

    // Ideal wind speed for kite flying: 8-24 mph
    const minWindSpeed = 8;
    const maxWindSpeed = 24;

    // Check for bad weather conditions
    const badWeatherConditions = ['rain', 'drizzle', 'thunderstorm', 'snow', 'storm'];
    const hasBadWeather = badWeatherConditions.some(condition =>
        weatherMain.includes(condition) || weatherDescription.includes(condition)
    );

    // Check for lightning/thunderstorm (dangerous!)
    if (weatherMain.includes('thunderstorm') || weatherDescription.includes('lightning')) {
        return {
            goodForKites: false,
            reason: '⚡ Thunderstorms detected - flying a kite is dangerous!'
        };
    }

    // Check for rain or snow
    if (hasBadWeather) {
        return {
            goodForKites: false,
            reason: `Current weather (${data.weather[0].description}) is not suitable for kite flying.`
        };
    }

    // Check wind speed
    if (windSpeed < minWindSpeed) {
        return {
            goodForKites: false,
            reason: `Wind speed is too low (${Math.round(windSpeed)} mph). Need at least ${minWindSpeed} mph.`
        };
    }

    if (windSpeed > maxWindSpeed) {
        return {
            goodForKites: false,
            reason: `Wind speed is too high (${Math.round(windSpeed)} mph). Safe limit is ${maxWindSpeed} mph.`
        };
    }

    // Perfect conditions!
    return {
        goodForKites: true,
        reason: `Perfect conditions! Wind speed: ${Math.round(windSpeed)} mph, Clear weather.`
    };
}

function showError(message) {
    errorDiv.textContent = message;
    errorDiv.classList.remove('hidden');
}

function hideError() {
    errorDiv.classList.add('hidden');
}

function showLoading() {
    loadingDiv.classList.remove('hidden');
}

function hideLoading() {
    loadingDiv.classList.add('hidden');
}

function showResults() {
    resultsDiv.classList.remove('hidden');
}

function hideResults() {
    resultsDiv.classList.add('hidden');
}

function capitalize(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}
