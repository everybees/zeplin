from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection


async def get_next_id(collection: AsyncIOMotorCollection) -> int:
    last_address = await collection.find_one(sort=[("_id", -1)])
    return 1 if last_address is None else last_address["_id"] + 1
