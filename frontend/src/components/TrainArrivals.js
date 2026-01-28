import React from 'react';

function TrainArrivals({ departures, stationName, loading, error, onRefresh }) {
    if (!stationName) {
        return (
            <div className="no-arrivals">
                <div className="no-arrivals-icon">🚉</div>
                <p>Select a station to see departures</p>
            </div>
        );
    }

    return (
        <div>
            <div className="arrivals-header">
                <h2 className="arrivals-station-name">🚄 {stationName}</h2>
                <button className="refresh-btn" onClick={onRefresh} disabled={loading}>
                    {loading ? 'Loading...' : '↻ Refresh'}
                </button>
            </div>

            {error && (
                <div className="error-message" style={{ marginBottom: '1rem' }}>
                    ⚠️ {error}
                </div>
            )}

            {loading && !departures.length ? (
                <div className="loading-overlay">
                    <div className="loading-spinner"></div>
                    <p style={{ marginTop: '0.5rem' }}>Fetching departures...</p>
                </div>
            ) : departures.length > 0 ? (
                <div>
                    {departures.map((departure, index) => (
                        <div
                            key={`${departure.destination}-${departure.minutes}-${index}`}
                            className="departure-item"
                            style={{ borderLeftColor: departure.hexcolor || '#4a90d9' }}
                        >
                            <div>
                                <div className="departure-destination">{departure.destination}</div>
                                <div className="departure-meta">
                                    <span>🚃 {departure.length} cars</span>
                                    <span>Platform {departure.platform}</span>
                                    <span style={{
                                        color: departure.hexcolor || '#4a90d9',
                                        fontWeight: 500
                                    }}>
                                        {departure.color} Line
                                    </span>
                                </div>
                            </div>
                            <div className="departure-time">
                                <span className={`departure-minutes ${departure.minutes === 'Leaving' ? 'arriving' : ''}`}>
                                    {departure.minutes === 'Leaving' ? 'NOW' : departure.minutes}
                                </span>
                                <span className="departure-label">
                                    {departure.minutes === 'Leaving' ? 'Departing' : 'min'}
                                </span>
                            </div>
                        </div>
                    ))}
                </div>
            ) : (
                <div className="no-arrivals">
                    <p>No departures scheduled</p>
                </div>
            )}
        </div>
    );
}

export default TrainArrivals;
