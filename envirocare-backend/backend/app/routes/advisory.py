from fastapi import APIRouter, Depends, Query, HTTPException, Header
from app.core.security import get_current_user
from app.db.mongodb import get_db
from app.services.risk_model import predict_risk
from app.services.lstm_trend import predict_trend
from app.services.environment_api import fetch_environment_data
from fastapi import Request

router = APIRouter(prefix="/ai", tags=["AI"])

def advice_by_risk(risk: float) -> str:
    if risk < 0.33:
        return "Outdoor activity is generally safe."
    elif risk < 0.66:
        return "Limit prolonged outdoor exposure."
    else:
        return "Stay indoors and use a mask if going out."

@router.get("/advisory")
async def get_advisory(
    request: Request,                     # <-- ADD THIS
    lat: float = Query(...),
    lon: float = Query(...),
    current_aqi: float = Query(...),
    prev1: float = Query(...),
    prev2: float = Query(...),
    prev3: float = Query(...),
    prev4: float = Query(...),
    current_user: dict = Depends(get_current_user),
):
    email = current_user["email"]

    db = get_db()
    health = await db.health.find_one({"email": email})
    if not health:
        raise HTTPException(status_code=404, detail="Create health profile first")

    baseline_risk = predict_risk(
        age=health["age"],
        has_asthma=health["has_asthma"],
        has_allergy=health["has_allergy"],
        sensitivity=health["sensitivity_level"],
    )

    trend = predict_trend([prev4, prev3, prev2, prev1, current_aqi])

    # Extract real token from header
    auth_header = request.headers.get("authorization")  # <-- IMPORTANT
    token = auth_header.replace("Bearer ", "") if auth_header else None

    env = await fetch_environment_data(
    token=token,   # internal call — no JWT needed
    lat=lat,
    lon=lon
)

    return {
        "email": email,
        "baseline_risk": baseline_risk,
        "predicted_next_aqi": trend,
        "temperature_c": env["temperature_c"],
        "windspeed_kmh": env["windspeed_kmh"],
        "aqi": env["aqi"],
        "location": env["location"],
        "advice": advice_by_risk(baseline_risk),
    }
