from fastapi import APIRouter, HTTPException
from app.schemas.user import UserCreate, UserResponse
from app.core.security import hash_password
from app.db.mongodb import get_db   # <-- IMPORTANT

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/signup", response_model=UserResponse)
async def signup(user: UserCreate):
    db = get_db()   # get DB at runtime

    if db is None:
        raise HTTPException(status_code=500, detail="Database not initialized")

    existing = await db["users"].find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed = hash_password(user.password)

    new_user = {
        "email": user.email,
        "password": hashed,
        "role": "user"
    }

    await db["users"].insert_one(new_user)

    return {"email": user.email}
