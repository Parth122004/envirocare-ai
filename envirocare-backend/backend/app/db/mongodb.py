from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

client = None
db = None

async def connect_to_mongo():
    global client, db

    client = AsyncIOMotorClient(
        settings.mongodb_uri,
        serverSelectionTimeoutMS=5000   # <-- IMPORTANT CHECK
    )

    # Force a real connection test
    await client.server_info()

    db = client[settings.database_name]
    print("✅ Connected to MongoDB Atlas")

async def close_mongo_connection():
    global client, db
    if client:
        client.close()
    db = None
    print("❌ MongoDB connection closed")

def get_db():
    return db
