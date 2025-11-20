from pymongo import AsyncMongoClient
from core.config import get_settings

# Singleton async client (recommended)
_async_client = AsyncMongoClient(get_settings().DB_URL)

async def get_client() -> AsyncMongoClient:
	return _async_client

async def get_collection(collection_name: str):
	client = await get_client()
	db = client["climatechart"]
	return db[collection_name]