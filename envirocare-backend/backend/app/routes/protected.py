from fastapi import APIRouter, Depends, HTTPException, status
from app.core.security import get_current_user

router = APIRouter(prefix="/protected", tags=["Protected"])

@router.get("/admin")
def admin_only(user = Depends(get_current_user)):
    if user.get("email") != "admin@example.com":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not an admin"
        )
    return {
        "email": user["email"],
        "role": "admin",
        "message": "Welcome Admin"
    }

@router.get("/user")
def normal_user(user = Depends(get_current_user)):
    return {
        "email": user["email"],
        "role": "user",
        "message": "Welcome User"
    }
