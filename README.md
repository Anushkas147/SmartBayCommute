# 🚄 BayCommute - SF Transit & Weather Hub

<div align="center">

![BayCommute Banner](https://img.shields.io/badge/🚄_BayCommute-SF_Transit_&_Weather-00d4ff?style=for-the-badge&labelColor=1a1a2e)

**Real-time BART departures + Weather + Air Quality in one dashboard**

[![API Mashup Mania 2026](https://img.shields.io/badge/🏆_API_Mashup-Mania_2026-blueviolet?style=flat-square)](https://github.com)
[![APIs Integrated](https://img.shields.io/badge/APIs-4_Integrated-success?style=flat-square)](https://github.com)
[![Made with React](https://img.shields.io/badge/React-18-61dafb?style=flat-square&logo=react)](https://reactjs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-Python-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-blue?style=flat-square)](LICENSE)

[Features](#-features) • [APIs Used](#-apis-integrated) • [Quick Start](#-quick-start) • [API Docs](#-api-endpoints) • [Screenshots](#-screenshots)

</div>

---

## 🎯 About The Project

**BayCommute** is a full-stack web application that combines **4 open-source APIs** to help San Francisco Bay Area commuters make informed travel decisions.

> **One app answers:** *"Should I take BART today? What's the weather? Is the air quality safe?"*

### The Problem
Commuters need to check multiple apps before leaving home - one for transit, one for weather, one for air quality. This wastes time and creates frustration.

### Our Solution
A unified dashboard that mashes up real-time transit data with weather and air quality information, giving commuters everything they need at a glance.

---

## 🔗 APIs Integrated

| API | Purpose | Key Required |
|-----|---------|:------------:|
| [**BART API**](https://api.bart.gov) | Real-time train departures, 49 stations | ✅ Public key (included) |
| [**Open Meteo Weather**](https://open-meteo.com) | Temperature, precipitation, wind | ✅ FREE |
| [**Open Meteo Air Quality**](https://open-meteo.com/en/docs/air-quality-api) | US EPA AQI, PM2.5, Ozone | ✅ FREE |
| [**Nominatim (OSM)**](https://nominatim.openstreetmap.org) | Location search & geocoding | ✅ FREE |

**✨ 3 out of 4 APIs require NO API key!**

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🗺️ **Interactive Map** | 49 BART stations plotted on OpenStreetMap with custom markers |
| 🚇 **Real-time Departures** | Live train ETAs with line colors (Red/Blue/Yellow/Green/Orange) |
| 🌡️ **Weather Dashboard** | Current temperature, precipitation, wind speed |
| 💨 **Air Quality Index** | EPA AQI with health level (Good/Moderate/Unhealthy) |
| 🔍 **Station Search** | Find BART stations instantly with live filtering |
| 📱 **Responsive Design** | Works seamlessly on mobile & desktop |
| ⚡ **Fast & Async** | Backend uses async Python for blazing fast API calls |

---

## 🛠️ Tech Stack

<table>
<tr>
<td align="center" width="50%">

### Frontend
![React](https://img.shields.io/badge/React-18-61dafb?style=for-the-badge&logo=react&logoColor=white)
![Leaflet](https://img.shields.io/badge/Leaflet-Maps-199900?style=for-the-badge&logo=leaflet&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-Flexbox-1572B6?style=for-the-badge&logo=css3&logoColor=white)

</td>
<td align="center" width="50%">

### Backend
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Uvicorn](https://img.shields.io/badge/Uvicorn-ASGI-499848?style=for-the-badge)

</td>
</tr>
</table>

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Installation

1️⃣ **Clone the repository**
```bash
git clone https://github.com/yourusername/baycommute.git
cd baycommute
```

2️⃣ **Setup Backend**
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

3️⃣ **Setup Frontend** (new terminal)
```bash
cd frontend
npm install
npm start
```

4️⃣ **Open in browser**
- 🌐 Frontend: http://localhost:3000
- 📡 API Docs: http://localhost:8000/docs

---

## 📡 API Endpoints

| Method | Endpoint | Description | Source API |
|:------:|----------|-------------|------------|
| `GET` | `/api/stations` | All 49 BART stations with GPS coordinates | BART |
| `GET` | `/api/departures/{station}` | Real-time train departures | BART |
| `GET` | `/api/weather` | Current SF weather | Open Meteo |
| `GET` | `/api/aqi` | Air Quality Index | Open Meteo |
| `GET` | `/api/search?q=` | Location search | Nominatim |

### Example Response - Weather
```json
{
  "success": true,
  "temperature": 62,
  "description": "Partly Cloudy",
  "icon": "⛅",
  "wind_speed": 12,
  "precipitation_mm": 0
}
```

### Example Response - AQI
```json
{
  "success": true,
  "aqi": 55,
  "aqi_level": "Moderate",
  "aqi_icon": "🟡",
  "pollutants": {
    "pm2_5": 12.3,
    "ozone": 45.6
  }
}
```

---

## 🎨 BART Line Colors

| Color | Line | Route |
|:-----:|------|-------|
| 🔴 | RED | Richmond ↔ Millbrae/SFO |
| 🔵 | BLUE | Dublin/Pleasanton ↔ Daly City |
| 🟡 | YELLOW | Antioch ↔ SFO/Millbrae |
| 🟢 | GREEN | Berryessa ↔ Daly City |
| 🟠 | ORANGE | Richmond ↔ Berryessa |

---

## 📁 Project Structure

```
baycommute/
├── 📂 backend/
│   ├── main.py              # FastAPI server (5 endpoints)
│   ├── requirements.txt     # Python dependencies
│   ├── .env                 # Environment variables
│   └── .env.example         # Template for env vars
│
├── 📂 frontend/
│   ├── package.json
│   ├── public/
│   │   └── index.html
│   └── src/
│       ├── App.js           # Main React component
│       ├── App.css          # Styling (600+ lines)
│       └── components/
│           ├── MapView.js       # Leaflet map integration
│           ├── StationList.js   # BART station selector
│           ├── TrainArrivals.js # Real-time departures
│           └── Weather.js       # Weather + AQI display
│
└── README.md
```

---

## 🧪 Testing the APIs

Using curl:
```bash
# Health check
curl http://localhost:8000/

# Get all stations
curl http://localhost:8000/api/stations

# Get departures for Embarcadero station
curl http://localhost:8000/api/departures/EMBR

# Get current weather
curl http://localhost:8000/api/weather

# Get air quality
curl http://localhost:8000/api/aqi

# Search for a location
curl "http://localhost:8000/api/search?q=mission"
```

Or visit the **interactive API docs** at: http://localhost:8000/docs

---

## 🏆 Built For

<div align="center">

### API MASHUP MANIA 2026
**ECSA × ALGORHYTHM**

*3-Hour Mini Hackathon | Build API-Powered Solutions*

</div>

---

## 🤝 Contributing

Contributions are welcome! Feel free to:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 👏 Acknowledgments

- [BART API](https://api.bart.gov) - Bay Area Rapid Transit
- [Open Meteo](https://open-meteo.com) - Free Weather & Air Quality API
- [OpenStreetMap](https://www.openstreetmap.org) - Map tiles & Nominatim
- [Leaflet.js](https://leafletjs.com) - Interactive maps library

---

<div align="center">

**Built with ❤️ for Bay Area commuters**

⭐ Star this repo if you find it useful!

</div>
