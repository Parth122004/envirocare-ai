from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import verify_password, create_access_token
from app.db.mongodb import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db = get_db()

    if db is None:
        raise HTTPException(status_code=500, detail="Database not initialized")

    user = await db["users"].find_one({"email": form_data.username})

    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # --- FIX: handle different possible field names ---
    stored_hash = (
        user.get("password")
        or user.get("hashed_password")
        or user.get("hash")
    )

    if not stored_hash:
        raise HTTPException(
            status_code=500,
            detail="Password hash missing in database"
        )

    if not verify_password(form_data.password, stored_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = create_access_token({"sub": user["email"]})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "email": user["email"]
    }
