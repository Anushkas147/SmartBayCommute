import React, { useEffect, useRef } from 'react';
import L from 'leaflet';

// San Francisco center coordinates
const SF_CENTER = [37.7749, -122.4194];
const DEFAULT_ZOOM = 12;

// Custom BART station icon
const createStationIcon = (isSelected) => {
    return L.divIcon({
        className: 'custom-marker-container',
        html: `
      <div class="custom-marker ${isSelected ? 'selected' : ''}">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="white">
          <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
        </svg>
      </div>
    `,
        iconSize: [32, 32],
        iconAnchor: [16, 32],
        popupAnchor: [0, -32]
    });
};

function MapView({ stations, selectedStation, onStationSelect }) {
    const mapRef = useRef(null);
    const mapInstanceRef = useRef(null);
    const markersRef = useRef({});

    // Initialize map
    useEffect(() => {
        if (!mapRef.current || mapInstanceRef.current) return;

        // Create map instance
        mapInstanceRef.current = L.map(mapRef.current, {
            center: SF_CENTER,
            zoom: DEFAULT_ZOOM,
            zoomControl: true
        });

        // Add OpenStreetMap tiles with dark theme
        L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
            subdomains: 'abcd',
            maxZoom: 19
        }).addTo(mapInstanceRef.current);

        // Cleanup on unmount
        return () => {
            if (mapInstanceRef.current) {
                mapInstanceRef.current.remove();
                mapInstanceRef.current = null;
            }
        };
    }, []);

    // Add station markers
    useEffect(() => {
        if (!mapInstanceRef.current || !stations.length) return;

        // Clear existing markers
        Object.values(markersRef.current).forEach(marker => {
            marker.remove();
        });
        markersRef.current = {};

        // Add markers for each station
        stations.forEach(station => {
            if (!station.lat || !station.lon) return;

            const isSelected = selectedStation?.abbr === station.abbr;
            const marker = L.marker([station.lat, station.lon], {
                icon: createStationIcon(isSelected)
            });

            // Create popup content
            const popupContent = `
        <div class="popup-content">
          <div class="popup-title">${station.name}</div>
          <div class="popup-subtitle">${station.city || 'San Francisco'}</div>
        </div>
      `;

            marker.bindPopup(popupContent);

            // Handle click
            marker.on('click', () => {
                onStationSelect(station);
            });

            marker.addTo(mapInstanceRef.current);
            markersRef.current[station.abbr] = marker;
        });
    }, [stations, selectedStation, onStationSelect]);

    // Update marker styles and pan to selected station
    useEffect(() => {
        if (!mapInstanceRef.current || !selectedStation) return;

        // Update all marker icons
        Object.entries(markersRef.current).forEach(([abbr, marker]) => {
            const isSelected = abbr === selectedStation.abbr;
            marker.setIcon(createStationIcon(isSelected));
        });

        // Pan to selected station
        if (selectedStation.lat && selectedStation.lon) {
            mapInstanceRef.current.flyTo([selectedStation.lat, selectedStation.lon], 14, {
                duration: 0.8
            });

            // Open popup
            const marker = markersRef.current[selectedStation.abbr];
            if (marker) {
                marker.openPopup();
            }
        }
    }, [selectedStation]);

    return <div ref={mapRef} style={{ width: '100%', height: '100%' }} />;
}

export default MapView;
