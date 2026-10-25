"""
Project 7: Weather API Dashboard
Consumes live public meteorological REST services with resilient offline fallback handling.
"""
from typing import Dict, Any
import requests

FALLBACK_STATIONS = {
    "rajkot": {
        "city": "Rajkot (Marwadi University)",
        "country": "India",
        "latitude": 22.3693,
        "longitude": 70.7981,
        "temperature_c": 29.4,
        "humidity_pct": 52,
        "wind_speed_kmh": 14.2,
        "condition": "Warm and Sunny",
        "forecast": [
            {"day": "Tomorrow", "high": 31.0, "low": 21.5, "condition": "Clear Sky"},
            {"day": "Day 2", "high": 30.5, "low": 22.0, "condition": "Partly Cloudy"},
            {"day": "Day 3", "high": 29.0, "low": 20.8, "condition": "Gentle Breeze"}
        ],
        "is_live": False,
        "source": "Pip Learn Meteorological Telemetry (Local Station)"
    },
    "ahmedabad": {
        "city": "Ahmedabad",
        "country": "India",
        "latitude": 23.0225,
        "longitude": 72.5714,
        "temperature_c": 31.0,
        "humidity_pct": 48,
        "wind_speed_kmh": 12.0,
        "condition": "Clear Sky",
        "forecast": [
            {"day": "Tomorrow", "high": 32.5, "low": 23.0, "condition": "Sunny"},
            {"day": "Day 2", "high": 32.0, "low": 22.5, "condition": "Clear"},
            {"day": "Day 3", "high": 31.0, "low": 21.0, "condition": "Sunny"}
        ],
        "is_live": False,
        "source": "Pip Learn Meteorological Telemetry (Local Station)"
    },
    "london": {
        "city": "London",
        "country": "United Kingdom",
        "latitude": 51.5074,
        "longitude": -0.1278,
        "temperature_c": 14.5,
        "humidity_pct": 74,
        "wind_speed_kmh": 18.5,
        "condition": "Overcast Mist",
        "forecast": [
            {"day": "Tomorrow", "high": 15.0, "low": 9.5, "condition": "Light Rain"},
            {"day": "Day 2", "high": 16.0, "low": 10.0, "condition": "Cloudy"},
            {"day": "Day 3", "high": 13.5, "low": 8.0, "condition": "Showers"}
        ],
        "is_live": False,
        "source": "Pip Learn Meteorological Telemetry (Local Station)"
    }
}

CITY_COORDINATES = {
    "rajkot": (22.3039, 70.8022, "Rajkot, India"),
    "ahmedabad": (23.0225, 72.5714, "Ahmedabad, India"),
    "mumbai": (19.0760, 72.8777, "Mumbai, India"),
    "delhi": (28.6139, 77.2090, "New Delhi, India"),
    "london": (51.5074, -0.1278, "London, UK"),
    "tokyo": (35.6762, 139.6503, "Tokyo, Japan"),
    "san francisco": (37.7749, -122.4194, "San Francisco, USA")
}

def get_weather_data(city_name: str = "Rajkot") -> Dict[str, Any]:
    """
    Query open-meteo.com public REST API with timeout.
    Falls back gracefully if network is unavailable.
    """
    key = city_name.strip().lower()
    coords = CITY_COORDINATES.get(key)

    if coords:
        lat, lon, label = coords
        endpoint = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "current_weather": "true",
            "daily": "temperature_2m_max,temperature_2m_min",
            "timezone": "auto"
        }
        try:
            resp = requests.get(endpoint, params=params, timeout=3.0)
            if resp.status_code == 200:
                data = resp.json()
                cur = data.get("current_weather", {})
                daily = data.get("daily", {})
                dates = daily.get("time", [])[1:4]
                max_temps = daily.get("temperature_2m_max", [])[1:4]
                min_temps = daily.get("temperature_2m_min", [])[1:4]

                forecast = []
                for d, hi, lo in zip(dates, max_temps, min_temps):
                    forecast.append({
                        "day": d,
                        "high": hi,
                        "low": lo,
                        "condition": "Seasonal Outlook"
                    })

                return {
                    "city": label,
                    "country": label.split(",")[-1].strip(),
                    "latitude": lat,
                    "longitude": lon,
                    "temperature_c": cur.get("temperature", 28.0),
                    "wind_speed_kmh": cur.get("windspeed", 10.0),
                    "humidity_pct": 55,
                    "condition": "Live REST Telemetry",
                    "forecast": forecast,
                    "is_live": True,
                    "source": "Open-Meteo Public REST API (Live)"
                }
        except Exception:
            # Fall through to cached offline station
            pass

    # Use fallback data
    fallback = FALLBACK_STATIONS.get(key, FALLBACK_STATIONS["rajkot"])
    return dict(fallback)
