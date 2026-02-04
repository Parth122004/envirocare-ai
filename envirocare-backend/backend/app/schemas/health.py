from pydantic import BaseModel

class HealthCreate(BaseModel):
    age: int
    has_asthma: bool
    has_allergy: bool
    sensitivity_level: float   # <-- FIXED (was string earlier)

class HealthResponse(HealthCreate):
    email: str
