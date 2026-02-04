from fastapi import APIRouter, Depends, HTTPException, status

from app.db.mongodb import get_db
from app.core.security import get_current_user
from app.schemas.health import HealthCreate, HealthResponse

router = APIRouter(prefix="/health", tags=["Health"])

@router.post("/", response_model=HealthResponse)
async def create_health(
    data: HealthCreate,
    current_user: dict = Depends(get_current_user),
    db = Depends(get_db),          # ← IMPORTANT FIX
):
    email = current_user["email"]

    existing = await db.health.find_one({"email": email})
    if existing:
        await db.health.delete_one({"email": email})

    record = data.dict()
    record["email"] = email

    await db.health.insert_one(record)
    return record

@router.get("/me", response_model=HealthResponse)
async def get_my_health(
    current_user: dict = Depends(get_current_user),
    db = Depends(get_db),          # ← ADD THIS
):
    email = current_user["email"]

    health = await db.health.find_one({"email": email})
    if not health:
        raise HTTPException(status_code=404, detail="Health profile not found")

    return health

@router.delete("/me")
async def delete_my_health(
    current_user: dict = Depends(get_current_user),
    db = Depends(get_db),          # ← ADD THIS
):
    email = current_user["email"]

    result = await db.health.delete_one({"email": email})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Health profile not found")

    return {"message": "Health profile deleted"}