from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.mongodb import connect_to_mongo, close_mongo_connection
from app.routes import user, auth, protected, health, environment, ai, advisory

app = FastAPI(
    title="EnviroCare AI Backend",
    description="AI-powered backend for environment-linked health risk alerts",
    version="1.0.0",
)

# --------- 🔹 ADD THIS BLOCK (VERY IMPORTANT) 🔹 ---------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],   # Vite frontend
    allow_credentials=True,
    allow_methods=["*"],     
    allow_headers=["*"],
)
# ---------------------------------------------------------

@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()

@app.get("/")
def root():
    return {"message": "EnviroCare AI backend is running successfully"}

# Include routes
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(protected.router)
app.include_router(health.router)
app.include_router(environment.router)
app.include_router(ai.router)
app.include_router(advisory.router)
