"""
San Francisco Transit & Weather API
FastAPI backend integrating BART API, Open Meteo, and OpenStreetMap Nominatim
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import httpx
import os
from typing import Optional

# Load environment variables
load_dotenv()

# API Configuration
# BART API - Public key (no signup needed)
BART_API_KEY = os.getenv("BART_API_KEY", "MW9S-E7SL-26DU-VV8V")

# API Base URLs
BART_BASE_URL = "http://api.bart.gov/api"
OPEN_METEO_BASE_URL = "https://api.open-meteo.com/v1"
OPEN_METEO_AQI_URL = "https://air-quality-api.open-meteo.com/v1"
NOMINATIM_BASE_URL = "https://nominatim.openstreetmap.org"

# San Francisco coordinates
SF_LAT = 37.7749
SF_LON = -122.4194

# Browser-like headers to avoid blocking
BROWSER_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
}

# Fallback BART station data (when API is unavailable)
FALLBACK_STATIONS = [
    {"abbr": "12TH", "name": "12th St. Oakland City Center", "lat": 37.803768, "lon": -122.271450, "city": "Oakland"},
    {"abbr": "16TH", "name": "16th St. Mission", "lat": 37.765062, "lon": -122.419694, "city": "San Francisco"},
    {"abbr": "19TH", "name": "19th St. Oakland", "lat": 37.808350, "lon": -122.268602, "city": "Oakland"},
    {"abbr": "24TH", "name": "24th St. Mission", "lat": 37.752254, "lon": -122.418466, "city": "San Francisco"},
    {"abbr": "ANTC", "name": "Antioch", "lat": 37.995388, "lon": -121.780420, "city": "Antioch"},
    {"abbr": "BALB", "name": "Balboa Park", "lat": 37.721981, "lon": -122.447414, "city": "San Francisco"},
    {"abbr": "BAYF", "name": "Bay Fair", "lat": 37.696924, "lon": -122.126514, "city": "San Leandro"},
    {"abbr": "BERY", "name": "Berryessa/North San José", "lat": 37.368473, "lon": -121.874564, "city": "San Jose"},
    {"abbr": "CAST", "name": "Castro Valley", "lat": 37.690746, "lon": -122.075602, "city": "Castro Valley"},
    {"abbr": "CIVC", "name": "Civic Center/UN Plaza", "lat": 37.779732, "lon": -122.414123, "city": "San Francisco"},
    {"abbr": "COLS", "name": "Coliseum", "lat": 37.753661, "lon": -122.196869, "city": "Oakland"},
    {"abbr": "COLM", "name": "Colma", "lat": 37.684638, "lon": -122.466233, "city": "Colma"},
    {"abbr": "CONC", "name": "Concord", "lat": 37.973737, "lon": -122.029095, "city": "Concord"},
    {"abbr": "DALY", "name": "Daly City", "lat": 37.706121, "lon": -122.469081, "city": "Daly City"},
    {"abbr": "DBRK", "name": "Downtown Berkeley", "lat": 37.869867, "lon": -122.268045, "city": "Berkeley"},
    {"abbr": "DUBL", "name": "Dublin/Pleasanton", "lat": 37.701687, "lon": -121.899179, "city": "Dublin"},
    {"abbr": "DELN", "name": "El Cerrito del Norte", "lat": 37.925086, "lon": -122.316794, "city": "El Cerrito"},
    {"abbr": "PLZA", "name": "El Cerrito Plaza", "lat": 37.902632, "lon": -122.298904, "city": "El Cerrito"},
    {"abbr": "EMBR", "name": "Embarcadero", "lat": 37.792976, "lon": -122.396742, "city": "San Francisco"},
    {"abbr": "FRMT", "name": "Fremont", "lat": 37.557465, "lon": -121.976608, "city": "Fremont"},
    {"abbr": "FTVL", "name": "Fruitvale", "lat": 37.774836, "lon": -122.224175, "city": "Oakland"},
    {"abbr": "GLEN", "name": "Glen Park", "lat": 37.733064, "lon": -122.433817, "city": "San Francisco"},
    {"abbr": "HAYW", "name": "Hayward", "lat": 37.669723, "lon": -122.087018, "city": "Hayward"},
    {"abbr": "LAFY", "name": "Lafayette", "lat": 37.893176, "lon": -122.123798, "city": "Lafayette"},
    {"abbr": "LAKE", "name": "Lake Merritt", "lat": 37.797484, "lon": -122.265609, "city": "Oakland"},
    {"abbr": "MCAR", "name": "MacArthur", "lat": 37.829065, "lon": -122.267040, "city": "Oakland"},
    {"abbr": "MLBR", "name": "Millbrae", "lat": 37.599787, "lon": -122.386749, "city": "Millbrae"},
    {"abbr": "MLPT", "name": "Milpitas", "lat": 37.410419, "lon": -121.891020, "city": "Milpitas"},
    {"abbr": "MONT", "name": "Montgomery St.", "lat": 37.789405, "lon": -122.401066, "city": "San Francisco"},
    {"abbr": "NBRK", "name": "North Berkeley", "lat": 37.874026, "lon": -122.283882, "city": "Berkeley"},
    {"abbr": "NCON", "name": "North Concord/Martinez", "lat": 38.002576, "lon": -122.024653, "city": "Concord"},
    {"abbr": "OAKL", "name": "Oakland International Airport", "lat": 37.713238, "lon": -122.212191, "city": "Oakland"},
    {"abbr": "ORIN", "name": "Orinda", "lat": 37.878361, "lon": -122.183791, "city": "Orinda"},
    {"abbr": "PCTR", "name": "Pittsburg Center", "lat": 38.016941, "lon": -121.889457, "city": "Pittsburg"},
    {"abbr": "PITT", "name": "Pittsburg/Bay Point", "lat": 38.018914, "lon": -121.945154, "city": "Pittsburg"},
    {"abbr": "PHIL", "name": "Pleasant Hill/Contra Costa Centre", "lat": 37.928468, "lon": -122.056012, "city": "Walnut Creek"},
    {"abbr": "POWL", "name": "Powell St.", "lat": 37.784991, "lon": -122.406857, "city": "San Francisco"},
    {"abbr": "RICH", "name": "Richmond", "lat": 37.936887, "lon": -122.353165, "city": "Richmond"},
    {"abbr": "ROCK", "name": "Rockridge", "lat": 37.844601, "lon": -122.251793, "city": "Oakland"},
    {"abbr": "SBRN", "name": "San Bruno", "lat": 37.637753, "lon": -122.416038, "city": "San Bruno"},
    {"abbr": "SFIA", "name": "San Francisco International Airport", "lat": 37.615966, "lon": -122.392409, "city": "San Francisco"},
    {"abbr": "SANL", "name": "San Leandro", "lat": 37.722619, "lon": -122.160881, "city": "San Leandro"},
    {"abbr": "SHAY", "name": "South Hayward", "lat": 37.634375, "lon": -122.057189, "city": "Hayward"},
    {"abbr": "SSAN", "name": "South San Francisco", "lat": 37.664174, "lon": -122.443870, "city": "South San Francisco"},
    {"abbr": "UCTY", "name": "Union City", "lat": 37.590630, "lon": -122.017867, "city": "Union City"},
    {"abbr": "WARM", "name": "Warm Springs/South Fremont", "lat": 37.502171, "lon": -121.939313, "city": "Fremont"},
    {"abbr": "WCRK", "name": "Walnut Creek", "lat": 37.905522, "lon": -122.067527, "city": "Walnut Creek"},
    {"abbr": "WDUB", "name": "West Dublin/Pleasanton", "lat": 37.699756, "lon": -121.928240, "city": "Dublin"},
    {"abbr": "WOAK", "name": "West Oakland", "lat": 37.804674, "lon": -122.294582, "city": "Oakland"},
]

# Sample departures for demo when API is unavailable
SAMPLE_DEPARTURES = {
    "EMBR": [
        {"destination": "Richmond", "minutes": "3", "platform": "2", "direction": "North", "length": "10", "color": "RED", "hexcolor": "#ff0000", "delay": "0"},
        {"destination": "Millbrae", "minutes": "6", "platform": "1", "direction": "South", "length": "10", "color": "RED", "hexcolor": "#ff0000", "delay": "0"},
        {"destination": "Berryessa", "minutes": "8", "platform": "2", "direction": "South", "length": "6", "color": "GREEN", "hexcolor": "#339933", "delay": "0"},
        {"destination": "Daly City", "minutes": "12", "platform": "1", "direction": "South", "length": "9", "color": "BLUE", "hexcolor": "#0099cc", "delay": "0"},
        {"destination": "Antioch", "minutes": "15", "platform": "2", "direction": "East", "length": "8", "color": "YELLOW", "hexcolor": "#ffff33", "delay": "0"},
    ],
    "POWL": [
        {"destination": "Richmond", "minutes": "5", "platform": "2", "direction": "North", "length": "10", "color": "RED", "hexcolor": "#ff0000", "delay": "0"},
        {"destination": "SFO Airport", "minutes": "7", "platform": "1", "direction": "South", "length": "10", "color": "YELLOW", "hexcolor": "#ffff33", "delay": "0"},
        {"destination": "Millbrae", "minutes": "10", "platform": "1", "direction": "South", "length": "10", "color": "RED", "hexcolor": "#ff0000", "delay": "0"},
        {"destination": "Dublin/Pleasanton", "minutes": "14", "platform": "2", "direction": "East", "length": "8", "color": "BLUE", "hexcolor": "#0099cc", "delay": "0"},
    ],
}

# Weather code to description mapping (Open Meteo WMO codes)
WEATHER_CODES = {
    0: {"description": "Clear Sky", "icon": "☀️"},
    1: {"description": "Mainly Clear", "icon": "🌤️"},
    2: {"description": "Partly Cloudy", "icon": "⛅"},
    3: {"description": "Overcast", "icon": "☁️"},
    45: {"description": "Foggy", "icon": "🌫️"},
    48: {"description": "Depositing Rime Fog", "icon": "🌫️"},
    51: {"description": "Light Drizzle", "icon": "🌧️"},
    53: {"description": "Moderate Drizzle", "icon": "🌧️"},
    55: {"description": "Dense Drizzle", "icon": "🌧️"},
    61: {"description": "Slight Rain", "icon": "🌧️"},
    63: {"description": "Moderate Rain", "icon": "🌧️"},
    65: {"description": "Heavy Rain", "icon": "🌧️"},
    71: {"description": "Slight Snow", "icon": "🌨️"},
    73: {"description": "Moderate Snow", "icon": "🌨️"},
    75: {"description": "Heavy Snow", "icon": "🌨️"},
    80: {"description": "Slight Rain Showers", "icon": "🌦️"},
    81: {"description": "Moderate Rain Showers", "icon": "🌦️"},
    82: {"description": "Violent Rain Showers", "icon": "⛈️"},
    95: {"description": "Thunderstorm", "icon": "⛈️"},
}

# AQI level descriptions (US EPA standard)
AQI_LEVELS = {
    (0, 50): {"level": "Good", "color": "#00e400", "icon": "🟢"},
    (51, 100): {"level": "Moderate", "color": "#ffff00", "icon": "🟡"},
    (101, 150): {"level": "Unhealthy for Sensitive Groups", "color": "#ff7e00", "icon": "🟠"},
    (151, 200): {"level": "Unhealthy", "color": "#ff0000", "icon": "🔴"},
    (201, 300): {"level": "Very Unhealthy", "color": "#8f3f97", "icon": "🟣"},
    (301, 500): {"level": "Hazardous", "color": "#7e0023", "icon": "⬛"},
}

def get_aqi_level(aqi: int) -> dict:
    """Get AQI level description based on US EPA standard"""
    for (low, high), info in AQI_LEVELS.items():
        if low <= aqi <= high:
            return info
    return {"level": "Unknown", "color": "#808080", "icon": "❓"}

# Initialize FastAPI
app = FastAPI(
    title="SF Transit & Weather API",
    description="API for BART real-time departures and San Francisco weather using Open Meteo",
    version="1.0.0"
)

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# HTTP client with timeout and browser headers
async def get_client():
    return httpx.AsyncClient(timeout=15.0, headers=BROWSER_HEADERS)


# ==================== HELPER FUNCTIONS ====================

def normalize_bart_stations(data: dict) -> list:
    """Normalize BART station data to consistent format"""
    try:
        stations = data.get("root", {}).get("stations", {}).get("station", [])
        return [
            {
                "abbr": s.get("abbr"),
                "name": s.get("name"),
                "lat": float(s.get("gtfs_latitude", 0)),
                "lon": float(s.get("gtfs_longitude", 0)),
                "address": s.get("address"),
                "city": s.get("city"),
                "zipcode": s.get("zipcode")
            }
            for s in stations
        ]
    except Exception:
        return []


def normalize_bart_departures(data: dict) -> dict:
    """Normalize BART departure data"""
    try:
        root = data.get("root", {})
        station = root.get("station", [{}])[0]
        etd_list = station.get("etd", [])
        
        departures = []
        for etd in etd_list:
            destination = etd.get("destination")
            for est in etd.get("estimate", []):
                departures.append({
                    "destination": destination,
                    "minutes": est.get("minutes"),
                    "platform": est.get("platform"),
                    "direction": est.get("direction"),
                    "length": est.get("length"),
                    "color": est.get("color"),
                    "hexcolor": est.get("hexcolor"),
                    "delay": est.get("delay")
                })
        
        return {
            "station_name": station.get("name"),
            "station_abbr": station.get("abbr"),
            "departures": departures
        }
    except Exception:
        return {"station_name": "", "station_abbr": "", "departures": []}


def normalize_open_meteo_weather(data: dict) -> dict:
    """Normalize Open Meteo weather data with user's exact format"""
    try:
        current_weather = data.get("current_weather", {})
        hourly = data.get("hourly", {})
        
        # Get weather code
        weather_code = current_weather.get("weathercode", 0)
        weather_info = WEATHER_CODES.get(weather_code, {"description": "Unknown", "icon": "❓"})
        
        # Temperature (already in Celsius from API)
        temp_c = current_weather.get("temperature", 0)
        temp_f = round((temp_c * 9/5) + 32)
        
        # Wind speed (in km/h from API)
        wind_kmh = current_weather.get("windspeed", 0)
        wind_mph = round(wind_kmh * 0.621371)
        
        # Get current hour precipitation (first hour)
        precipitation = hourly.get("precipitation", [0])[0] if hourly.get("precipitation") else 0
        rain = hourly.get("rain", [0])[0] if hourly.get("rain") else 0
        
        return {
            "city": "San Francisco",
            "temperature": temp_f,
            "temperature_c": round(temp_c),
            "description": weather_info["description"],
            "icon": weather_info["icon"],
            "wind_speed": wind_mph,
            "wind_speed_kmh": round(wind_kmh),
            "wind_direction": current_weather.get("winddirection", 0),
            "weather_code": weather_code,
            "precipitation_mm": precipitation,
            "rain_mm": rain,
            "is_day": current_weather.get("is_day", 1)
        }
    except Exception:
        return {}


# ==================== API ENDPOINTS ====================

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "message": "SF Transit & Weather API is running",
        "apis_used": {
            "transit": "BART API (api.bart.gov)",
            "weather": "Open Meteo (api.open-meteo.com) - FREE, no key needed",
            "geocoding": "Nominatim (nominatim.openstreetmap.org) - FREE, no key needed"
        },
        "endpoints": {
            "stations": "/api/stations",
            "departures": "/api/departures/{station_abbr}",
            "weather": "/api/weather",
            "aqi": "/api/aqi",
            "search": "/api/search?q={query}"
        }
    }


@app.get("/api/stations")
async def get_stations():
    """
    Get list of all BART stations with coordinates
    Falls back to cached data if API is unavailable
    """
    async with await get_client() as client:
        try:
            response = await client.get(
                f"{BART_BASE_URL}/stn.aspx",
                params={
                    "cmd": "stns",
                    "key": BART_API_KEY,
                    "json": "y"
                }
            )
            response.raise_for_status()
            
            # Check if response is HTML (Cloudflare challenge)
            content_type = response.headers.get("content-type", "")
            if "text/html" in content_type:
                raise Exception("Cloudflare challenge detected")
            
            data = response.json()
            stations = normalize_bart_stations(data)
            
            if stations:
                return {
                    "success": True,
                    "count": len(stations),
                    "stations": stations,
                    "source": "live"
                }
            else:
                raise Exception("Empty response from BART API")
                
        except Exception as e:
            # Fallback to cached data
            return {
                "success": True,
                "count": len(FALLBACK_STATIONS),
                "stations": FALLBACK_STATIONS,
                "source": "cached",
                "note": "Using cached station data (API temporarily unavailable)"
            }


@app.get("/api/departures/{station_abbr}")
async def get_departures(station_abbr: str):
    """
    Get real-time train departures for a specific BART station
    Falls back to sample data if API is unavailable
    
    - **station_abbr**: 4-letter station abbreviation (e.g., EMBR, POWL, 16TH)
    """
    station_abbr = station_abbr.upper()
    station_name = next((s["name"] for s in FALLBACK_STATIONS if s["abbr"] == station_abbr), station_abbr)
    
    async with await get_client() as client:
        try:
            response = await client.get(
                f"{BART_BASE_URL}/etd.aspx",
                params={
                    "cmd": "etd",
                    "orig": station_abbr,
                    "key": BART_API_KEY,
                    "json": "y"
                }
            )
            response.raise_for_status()
            
            # Check if response is HTML (Cloudflare challenge)
            content_type = response.headers.get("content-type", "")
            if "text/html" in content_type:
                raise Exception("Cloudflare challenge detected")
            
            data = response.json()
            
            # Check for API error
            if "error" in data.get("root", {}):
                error_msg = data["root"]["error"].get("message", "Unknown error")
                raise HTTPException(status_code=400, detail=error_msg)
            
            departures = normalize_bart_departures(data)
            
            return {
                "success": True,
                "source": "live",
                **departures
            }
            
        except HTTPException:
            raise
        except Exception as e:
            # Fallback to sample data
            sample = SAMPLE_DEPARTURES.get(station_abbr, SAMPLE_DEPARTURES.get("EMBR", []))
            return {
                "success": True,
                "station_name": station_name,
                "station_abbr": station_abbr,
                "departures": sample,
                "source": "demo",
                "note": "Demo data - API temporarily unavailable"
            }


@app.get("/api/weather")
async def get_weather():
    """
    Get current weather for San Francisco using Open Meteo API
    URL: https://api.open-meteo.com/v1/forecast?latitude=37.7749&longitude=-122.4194&current_weather=true&hourly=precipitation,rain&timezone=America/Los_Angeles
    Open Meteo is FREE and requires NO API key
    """
    async with await get_client() as client:
        try:
            response = await client.get(
                f"{OPEN_METEO_BASE_URL}/forecast",
                params={
                    "latitude": SF_LAT,
                    "longitude": SF_LON,
                    "current_weather": "true",
                    "hourly": "precipitation,rain",
                    "timezone": "America/Los_Angeles"
                }
            )
            response.raise_for_status()
            data = response.json()
            weather = normalize_open_meteo_weather(data)
            
            return {
                "success": True,
                "source": "live",
                "api": "Open Meteo (FREE)",
                **weather
            }
        except httpx.HTTPError as e:
            raise HTTPException(status_code=502, detail=f"Weather API error: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")


@app.get("/api/aqi")
async def get_aqi():
    """
    Get Air Quality Index (AQI) for San Francisco using Open Meteo Air Quality API
    Open Meteo Air Quality is FREE and requires NO API key
    """
    async with await get_client() as client:
        try:
            response = await client.get(
                f"{OPEN_METEO_AQI_URL}/air-quality",
                params={
                    "latitude": SF_LAT,
                    "longitude": SF_LON,
                    "current": "us_aqi,pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,ozone",
                    "timezone": "America/Los_Angeles"
                }
            )
            response.raise_for_status()
            data = response.json()
            
            current = data.get("current", {})
            aqi_value = current.get("us_aqi", 0)
            aqi_info = get_aqi_level(aqi_value)
            
            return {
                "success": True,
                "source": "live",
                "api": "Open Meteo Air Quality (FREE)",
                "city": "San Francisco",
                "aqi": aqi_value,
                "aqi_level": aqi_info["level"],
                "aqi_color": aqi_info["color"],
                "aqi_icon": aqi_info["icon"],
                "pollutants": {
                    "pm2_5": current.get("pm2_5", 0),
                    "pm10": current.get("pm10", 0),
                    "ozone": current.get("ozone", 0),
                    "nitrogen_dioxide": current.get("nitrogen_dioxide", 0),
                    "carbon_monoxide": current.get("carbon_monoxide", 0)
                }
            }
        except httpx.HTTPError as e:
            raise HTTPException(status_code=502, detail=f"AQI API error: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")


@app.get("/api/search")
async def search_location(q: str = Query(..., min_length=2, description="Search query")):
    """
    Search for locations in San Francisco Bay Area using OpenStreetMap Nominatim
    Nominatim is FREE and requires NO API key
    
    - **q**: Search query (e.g., "Golden Gate Bridge", "Mission District")
    """
    async with await get_client() as client:
        try:
            response = await client.get(
                f"{NOMINATIM_BASE_URL}/search",
                params={
                    "q": f"{q}, San Francisco, CA",
                    "format": "json",
                    "limit": 5,
                    "addressdetails": 1
                },
                headers={
                    "User-Agent": "SFTransitWeatherApp/1.0 (transit-demo)"
                }
            )
            response.raise_for_status()
            results = response.json()
            
            # Normalize results
            locations = [
                {
                    "name": r.get("display_name"),
                    "lat": float(r.get("lat", 0)),
                    "lon": float(r.get("lon", 0)),
                    "type": r.get("type"),
                    "importance": r.get("importance")
                }
                for r in results
            ]
            
            return {
                "success": True,
                "query": q,
                "count": len(locations),
                "results": locations,
                "api": "Nominatim (FREE)"
            }
        except httpx.HTTPError as e:
            raise HTTPException(status_code=502, detail=f"Geocoding API error: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")


# Run with: uvicorn main:app --reload --port 8000
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
