import httpx

WEATHER_BASE = "http://127.0.0.1:8000/environment/weather"
AQI_BASE = "http://127.0.0.1:8000/environment/aqi"

async def fetch_environment_data(token: str | None, lat: float, lon: float):

    headers = {}
    if token:                     # <-- only attach header if token exists
        headers["Authorization"] = f"Bearer {token}"

    async with httpx.AsyncClient(timeout=10.0) as client:

        weather_res = await client.get(
            WEATHER_BASE,
            params={"lat": lat, "lon": lon},
            headers=headers
        )

        aqi_res = await client.get(
            AQI_BASE,
            params={"lat": lat, "lon": lon},
            headers=headers
        )

    # If still unauthorized, return fallback instead of crashing
    if weather_res.status_code == 401 or aqi_res.status_code == 401:
        return {
            "temperature_c": None,
            "windspeed_kmh": None,
            "aqi": None,
            "location": "Unavailable (auth issue)"
        }

    if weather_res.status_code != 200 or aqi_res.status_code != 200:
        raise Exception("Failed to fetch environment data")

    weather = weather_res.json()
    aqi = aqi_res.json()

    return {
        "temperature_c": weather["temperature_c"],
        "windspeed_kmh": weather["windspeed_kmh"],
        "aqi": aqi["aqi"],
        "location": aqi["location"]
    }
