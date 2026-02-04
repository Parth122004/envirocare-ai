from pydantic import BaseModel
from typing import Optional


class HealthCreate(BaseModel):
    age: int
    has_asthma: bool
    has_allergy: bool
    sensitivity_level: str  # "low", "medium", "high"


class HealthInDB(HealthCreate):
    email: str


class HealthResponse(HealthCreate):
    email: str
