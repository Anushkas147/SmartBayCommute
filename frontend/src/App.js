import React, { useState, useEffect } from 'react';
import './App.css';
import MapView from './components/MapView';
import StationList from './components/StationList';
import TrainArrivals from './components/TrainArrivals';
import Weather from './components/Weather';

// API Base URL
const API_BASE = 'http://localhost:8000';

function App() {
    // State
    const [stations, setStations] = useState([]);
    const [selectedStation, setSelectedStation] = useState(null);
    const [departures, setDepartures] = useState([]);
    const [weather, setWeather] = useState(null);
    const [aqi, setAqi] = useState(null);
    const [searchQuery, setSearchQuery] = useState('');
    const [loading, setLoading] = useState({ stations: true, departures: false, weather: true, aqi: true });
    const [error, setError] = useState({ stations: null, departures: null, weather: null, aqi: null });

    // Fetch BART stations on mount
    useEffect(() => {
        fetchStations();
        fetchWeather();
        fetchAqi();
    }, []);

    // Fetch departures when station is selected
    useEffect(() => {
        if (selectedStation) {
            fetchDepartures(selectedStation.abbr);
        }
    }, [selectedStation]);

    // API Calls
    const fetchStations = async () => {
        try {
            setLoading(prev => ({ ...prev, stations: true }));
            setError(prev => ({ ...prev, stations: null }));

            const response = await fetch(`${API_BASE}/api/stations`);
            if (!response.ok) throw new Error('Failed to fetch stations');

            const data = await response.json();
            setStations(data.stations || []);
        } catch (err) {
            setError(prev => ({ ...prev, stations: err.message }));
        } finally {
            setLoading(prev => ({ ...prev, stations: false }));
        }
    };

    const fetchDepartures = async (stationAbbr) => {
        try {
            setLoading(prev => ({ ...prev, departures: true }));
            setError(prev => ({ ...prev, departures: null }));

            const response = await fetch(`${API_BASE}/api/departures/${stationAbbr}`);
            if (!response.ok) throw new Error('Failed to fetch departures');

            const data = await response.json();
            setDepartures(data.departures || []);
        } catch (err) {
            setError(prev => ({ ...prev, departures: err.message }));
            setDepartures([]);
        } finally {
            setLoading(prev => ({ ...prev, departures: false }));
        }
    };

    const fetchWeather = async () => {
        try {
            setLoading(prev => ({ ...prev, weather: true }));
            setError(prev => ({ ...prev, weather: null }));

            const response = await fetch(`${API_BASE}/api/weather`);
            if (!response.ok) {
                const errData = await response.json();
                throw new Error(errData.detail || 'Failed to fetch weather');
            }

            const data = await response.json();
            setWeather(data);
        } catch (err) {
            setError(prev => ({ ...prev, weather: err.message }));
        } finally {
            setLoading(prev => ({ ...prev, weather: false }));
        }
    };

    const fetchAqi = async () => {
        try {
            setLoading(prev => ({ ...prev, aqi: true }));
            setError(prev => ({ ...prev, aqi: null }));

            const response = await fetch(`${API_BASE}/api/aqi`);
            if (!response.ok) {
                const errData = await response.json();
                throw new Error(errData.detail || 'Failed to fetch AQI');
            }

            const data = await response.json();
            setAqi(data);
        } catch (err) {
            setError(prev => ({ ...prev, aqi: err.message }));
        } finally {
            setLoading(prev => ({ ...prev, aqi: false }));
        }
    };

    // Handle station selection
    const handleStationSelect = (station) => {
        setSelectedStation(station);
    };

    // Filter stations based on search
    const filteredStations = stations.filter(station =>
        station.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        station.city?.toLowerCase().includes(searchQuery.toLowerCase())
    );

    // Refresh departures
    const handleRefresh = () => {
        if (selectedStation) {
            fetchDepartures(selectedStation.abbr);
        }
    };

    return (
        <div className="app-container">
            {/* Header */}
            <header className="header">
                <div>
                    <h1>🚄 SF Transit & Weather</h1>
                    <p className="header-subtitle">Real-time BART departures • San Francisco</p>
                </div>
            </header>

            {/* Main Content */}
            <div className="main-content">
                {/* Sidebar */}
                <aside className="sidebar">
                    {/* Weather Section */}
                    <section className="sidebar-section">
                        <h2 className="section-title">☀️ San Francisco Weather</h2>
                        <Weather
                            weather={weather}
                            aqi={aqi}
                            loading={loading.weather}
                            loadingAqi={loading.aqi}
                            error={error.weather}
                        />
                    </section>

                    {/* Station Search */}
                    <section className="sidebar-section">
                        <h2 className="section-title">🔍 Find Station</h2>
                        <div className="search-container">
                            <input
                                type="text"
                                className="search-input"
                                placeholder="Search BART stations..."
                                value={searchQuery}
                                onChange={(e) => setSearchQuery(e.target.value)}
                            />
                        </div>
                    </section>

                    {/* Station List */}
                    <section className="sidebar-section">
                        <h2 className="section-title">🚉 BART Stations ({filteredStations.length})</h2>
                        <StationList
                            stations={filteredStations}
                            selectedStation={selectedStation}
                            onSelect={handleStationSelect}
                            loading={loading.stations}
                            error={error.stations}
                        />
                    </section>

                    {/* Train Arrivals */}
                    <div className="arrivals-container">
                        <TrainArrivals
                            departures={departures}
                            stationName={selectedStation?.name}
                            loading={loading.departures}
                            error={error.departures}
                            onRefresh={handleRefresh}
                        />
                    </div>
                </aside>

                {/* Map */}
                <div className="map-container">
                    <MapView
                        stations={stations}
                        selectedStation={selectedStation}
                        onStationSelect={handleStationSelect}
                    />
                </div>
            </div>
        </div>
    );
}

export default App;
