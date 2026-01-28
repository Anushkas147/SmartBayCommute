import React from 'react';

// Weather icon mapping - handles both Open Meteo codes and fallback
const getWeatherIcon = (icon, weatherCode) => {
    // If icon is an emoji, use it directly
    if (icon && icon.length <= 4 && /[\u{1F300}-\u{1F9FF}]/u.test(icon)) {
        return icon;
    }

    // Fallback: Map weather codes to emojis
    const codeMap = {
        0: '☀️',   // Clear
        1: '🌤️',  // Mainly clear
        2: '⛅',   // Partly cloudy
        3: '☁️',   // Overcast
        45: '🌫️', // Fog
        48: '🌫️', // Rime fog
        51: '🌧️', // Drizzle
        53: '🌧️',
        55: '🌧️',
        61: '🌧️', // Rain
        63: '🌧️',
        65: '🌧️',
        71: '🌨️', // Snow
        73: '🌨️',
        75: '🌨️',
        80: '🌦️', // Showers
        81: '🌦️',
        82: '⛈️',
        95: '⛈️', // Thunderstorm
    };

    return codeMap[weatherCode] || '☀️';
};

function Weather({ weather, aqi, loading, loadingAqi, error }) {
    if (loading) {
        return (
            <div className="weather-loading">
                <div className="loading-spinner"></div>
                <p style={{ marginTop: '0.5rem' }}>Loading weather...</p>
            </div>
        );
    }

    if (error) {
        return (
            <div className="weather-error">
                <p>⚠️ {error}</p>
            </div>
        );
    }

    if (!weather) {
        return (
            <div className="weather-loading">
                <p>No weather data available</p>
            </div>
        );
    }

    const weatherIcon = getWeatherIcon(weather.icon, weather.weather_code);

    return (
        <div className="weather-section">
            {/* Weather Card */}
            <div className="weather-card">
                <div className="weather-icon-emoji">{weatherIcon}</div>
                <div className="weather-info">
                    <h3>{weather.temperature}°F</h3>
                    <p className="weather-description">{weather.description}</p>
                    <div className="weather-details">
                        <span>💨 {weather.wind_speed} mph</span>
                        <span>🌧️ {weather.precipitation_mm || 0} mm</span>
                    </div>
                </div>
            </div>

            {/* AQI Card */}
            {aqi && (
                <div className="aqi-card" style={{ borderLeftColor: aqi.aqi_color }}>
                    <div className="aqi-header">
                        <span className="aqi-icon">{aqi.aqi_icon}</span>
                        <span className="aqi-label">Air Quality Index</span>
                    </div>
                    <div className="aqi-value">
                        <span className="aqi-number" style={{ color: aqi.aqi_color }}>{aqi.aqi}</span>
                        <span className="aqi-level">{aqi.aqi_level}</span>
                    </div>
                    <div className="aqi-pollutants">
                        <span>PM2.5: {aqi.pollutants?.pm2_5?.toFixed(1)} µg/m³</span>
                        <span>O₃: {aqi.pollutants?.ozone?.toFixed(1)} µg/m³</span>
                    </div>
                </div>
            )}

            {loadingAqi && !aqi && (
                <div className="aqi-loading">
                    <div className="loading-spinner"></div>
                    <span>Loading AQI...</span>
                </div>
            )}
        </div>
    );
}

export default Weather;
