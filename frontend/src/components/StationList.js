import React from 'react';

function StationList({ stations, selectedStation, onSelect, loading, error }) {
    if (loading) {
        return (
            <div className="loading-overlay">
                <div className="loading-spinner"></div>
                <p style={{ marginTop: '0.5rem' }}>Loading stations...</p>
            </div>
        );
    }

    if (error) {
        return (
            <div className="error-message">
                ⚠️ {error}
            </div>
        );
    }

    if (!stations.length) {
        return (
            <div className="no-arrivals">
                <p>No stations found</p>
            </div>
        );
    }

    return (
        <div className="station-list">
            {stations.map(station => (
                <div
                    key={station.abbr}
                    className={`station-item ${selectedStation?.abbr === station.abbr ? 'selected' : ''}`}
                    onClick={() => onSelect(station)}
                >
                    <div className="station-marker"></div>
                    <div>
                        <div className="station-name">{station.name}</div>
                        <div className="station-city">{station.city || 'San Francisco'}</div>
                    </div>
                </div>
            ))}
        </div>
    );
}

export default StationList;
