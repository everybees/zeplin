from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

from core.config import CURRENCY_COLLECTION_NAME, PRIVATE_KEY_COLLECTION_NAME, MONGODB_URL, DB_NAME, CURRENCIES


app = FastAPI()


@app.on_event("startup")
async def startup_db_client():
    try:
        app.mongodb_client = AsyncIOMotorClient(MONGODB_URL)
        app.mongodb = app.mongodb_client.get_database(DB_NAME)
        app.currency_collections = {}
        app.private_key_collections = {}

        for currency in CURRENCIES:
            currency_collection_name = f"{currency}-{CURRENCY_COLLECTION_NAME}"
            private_key_collection_name = f"{currency}-{PRIVATE_KEY_COLLECTION_NAME}"

            app.currency_collections[currency] = app.mongodb.get_collection(currency_collection_name)
            app.private_key_collections[currency] = app.mongodb.get_collection(private_key_collection_name)

        print("Database connected")
    except Exception as e:
        print(f"Error connecting to database: {e}")


@app.on_event("shutdown")
async def shutdown_db_client():
    if hasattr(app, "mongodb_client"):
        app.mongodb_client.close()
        print("Database connection closed")


async def get_next_id(collection: AsyncIOMotorCollection) -> int:
    last_address = await collection.find_one(sort=[("_id", -1)])
    return 1 if last_address is None else last_address["_id"] + 1
