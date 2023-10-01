from datetime import datetime
from typing import List

from fastapi import APIRouter, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient

from core.config import MONGODB_URL, PRIVATE_KEY_COLLECTION_NAME, CURRENCY_COLLECTION_NAME
from db.mongodb import get_next_id
from models.models import CryptoCurrency, Address
from services.crypto_service import generate_address

router = APIRouter()

db_client = AsyncIOMotorClient(MONGODB_URL)
db = db_client.get_database()
currency_collection = db.get_collection(CURRENCY_COLLECTION_NAME)
private_key_collection = db.get_collection(PRIVATE_KEY_COLLECTION_NAME)


@router.post("/address/{currency}", response_model=Address)
async def create_addresses(currency: CryptoCurrency):
    try:
        if currency not in ["BTC", "ETH"]:
            raise HTTPException(status_code=400, detail="Invalid currency")

        private_key, encryption_key, address = generate_address(currency)
        date_created = datetime.utcnow()
        next_id = await get_next_id(currency_collection)

        await private_key_collection.insert_one({
            "encrypted_private_key": private_key,
            "encryption_key": encryption_key,
            "currency": currency
        })

        await currency_collection.insert_one({
            "_id": next_id,
            "address": address,
            "currency": currency,
            "date_created": date_created
        })

        return Address(
            id=next_id,
            address=address,
            currency=currency,
            date_created=date_created
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Server error") from e


@router.get(
    "/address/", response_model=List[Address])
async def list_addresses():
    try:
        addresses = []
        async for address in currency_collection.find():
            addresses.append(Address(
                address=address["address"],
                currency=address["currency"],
                id=address["_id"],
                date_created=address["date_created"]
            ))
        return addresses
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Server error {e}") from e


@router.get("/address/{id}", response_model=List[Address])
async def retrieve_address(
        id: int,
):
    try:
        addresses = []
        async for address in currency_collection.find({"_id": id}):
            addresses.append(Address(
                address=address["address"],
                currency=address["currency"],
                id=address["_id"],
                date_created=address["date_created"]
            ))
        return addresses
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Server error {e}") from e


@router.get("/private_key/")
async def retrieve_private_key():
    try:
        private_keys = []
        async for private_key in private_key_collection.find():
            private_keys.append({
                "encrypted_private_key": private_key["encrypted_private_key"],
                "encryption_key": private_key["encryption_key"],
                "currency": private_key["currency"]
            })
        return private_keys
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Server error {e}") from e
