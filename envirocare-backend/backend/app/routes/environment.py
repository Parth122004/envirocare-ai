from fastapi import APIRouter, Depends, Query, HTTPException
import httpx

from app.core.security import get_current_user
from app.core.config import settings

router = APIRouter(prefix="/environment", tags=["Environment"])

# -------- BASE URLS --------
OPEN_METEO_BASE = "https://api.open-meteo.com/v1/forecast"
IQAIR_NEAREST = "https://api.airvisual.com/v2/nearest_city"


# ===========================
# WEATHER (UNCHANGED)
# ===========================
@router.get("/weather")
async def get_weather(
    lat: float = Query(18.5204, description="Latitude (default Pune)"),
    lon: float = Query(73.8567, description="Longitude (default Pune)"),
    current_user: dict = Depends(get_current_user),
):
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": True,
        "temperature_unit": "celsius",
        "windspeed_unit": "kmh"
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        r = await client.get(OPEN_METEO_BASE, params=params)

    if r.status_code != 200:
        raise HTTPException(
            status_code=500,
            detail=f"Open-Meteo error: {r.status_code}"
        )

    data = r.json()

    if "current_weather" not in data:
        raise HTTPException(
            status_code=500,
            detail="Invalid response from Open-Meteo"
        )

    return {
        "temperature_c": data["current_weather"]["temperature"],
        "windspeed_kmh": data["current_weather"]["windspeed"],
        "location": f"{lat}, {lon}",
        "user": current_user["email"],
        "source": "Open-Meteo"
    }


# ===========================
# AQI — FIXED VERSION (WORKS)
# ===========================
@router.get("/aqi")
async def get_aqi(
    lat: float = Query(18.5204, description="Latitude (default Pune)"),
    lon: float = Query(73.8567, description="Longitude (default Pune)"),
    current_user: dict = Depends(get_current_user),
):

    if not settings.iqair_api_key:
        raise HTTPException(
            status_code=500,
            detail="Set IQAIR_API_KEY in backend/.env first"
        )

    params = {
        "lat": lat,
        "lon": lon,
        "key": settings.iqair_api_key
    }

    async with httpx.AsyncClient() as client:
        r = await client.get(IQAIR_NEAREST, params=params)

    if r.status_code != 200:
        raise HTTPException(status_code=500, detail="IQAir service failed")

    data = r.json()

    aqi = data["data"]["current"]["pollution"]["aqius"]
    city = data["data"]["city"]
    state = data["data"]["state"]
    country = data["data"]["country"]

    return {
        "aqi": aqi,
        "location": f"{city}, {state}, {country}",
        "user": current_user["email"],
        "source": "IQAir"
    }

import httpx

async def fetch_weather(lat: float, lon: float):
    url = (
        "https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}&current_weather=true"
    )

    async with httpx.AsyncClient() as client:
        resp = await client.get(url)

    data = resp.json()

    cw = data.get("current_weather", {})

    return {
        "temperature_c": cw.get("temperature"),
        "windspeed_kmh": cw.get("windspeed"),
        "location": f"{lat}, {lon}",
        "source": "Open-Meteo",
    }