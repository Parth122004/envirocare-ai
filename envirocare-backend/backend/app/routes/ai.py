from fastapi import APIRouter, Depends, Query, HTTPException
from app.core.security import get_current_user
from app.db.mongodb import get_db
from app.services.risk_model import predict_risk
from app.services.lstm_trend import predict_trend

router = APIRouter(prefix="/ai", tags=["AI"])

def interpret_risk(score: float) -> str:
    if score < 0.33:
        return "Low"
    elif score < 0.66:
        return "Medium"
    else:
        return "High"

@router.get("/risk")
async def get_personal_risk(
    lat: float = Query(...),
    lon: float = Query(...),
    current_user: dict = Depends(get_current_user),
):
    email = current_user["email"]

    health = await get_db().health.find_one({"email": email})
    if not health:
        raise HTTPException(status_code=404, detail="Create health profile first")

    risk = predict_risk(
        age=health["age"],
        has_asthma=health["has_asthma"],
        has_allergy=health["has_allergy"],
        sensitivity=health["sensitivity_level"],
    )

    return {
        "email": email,
        "baseline_risk": risk,
        "risk_level": interpret_risk(risk),
        "model": "XGBoost (v1)"
    }

@router.get("/trend")
async def get_environment_trend(
    current_aqi: float = Query(...),
    prev1: float = Query(...),
    prev2: float = Query(...),
    prev3: float = Query(...),
    prev4: float = Query(...),
    current_user: dict = Depends(get_current_user),
):
    values = [prev4, prev3, prev2, prev1, current_aqi]
    prediction = predict_trend(values)

    return {
        "predicted_next_aqi": prediction,
        "method": "LSTM (time-series)"
    }
