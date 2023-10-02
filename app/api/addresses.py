from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query

from core.config import CURRENCIES
from db.mongodb import get_next_id
from models.addresses import Address
from services.crypto_service import generate_address

from db.mongodb import app

router = APIRouter()


@router.post("/address/{currency}", response_model=Address)
async def create_addresses(currency: str):
    try:
        if currency.lower() not in CURRENCIES:
            raise HTTPException(status_code=400, detail="Invalid currency")
        currency = currency.lower()
        next_id = await get_next_id(app.currency_collections[currency])
        print(next_id, "NEXT_ID")
        private_key, encryption_key, address = generate_address(currency)
        date_created = datetime.utcnow()

        await app.private_key_collections[currency].insert_one({
            "encrypted_private_key": private_key,
            "encryption_key": encryption_key,
            "currency": currency
        })

        await app.currency_collections[currency].insert_one({
            "_id": next_id,
            "address": address,
            "currency": currency,
            "date_created": date_created
        })

        print(private_key, encryption_key, address)

        return Address(
            id=next_id,
            address=address,
            currency=currency,
            date_created=date_created
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Server error") from e


@router.get("/address", response_model=List[Address])
async def list_addresses(currency: Optional[str] = Query(None)):
    try:
        addresses = []
        if currency and CURRENCIES.get(currency.lower()):
            currency = currency.lower()
            async for address in app.currency_collections[currency].find():
                addresses.append(Address(
                    address=address["address"],
                    currency=address["currency"],
                    id=address["_id"],
                    date_created=address["date_created"]
                ))
            return addresses

        for currency in CURRENCIES:
            async for address in app.currency_collections[currency].find():
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


@router.get("/address/{currency}/{id}", response_model=List[Address])
async def retrieve_address(
        id: int, currency: str
):
    try:
        addresses = []
        currency = currency.lower()
        async for address in app.currency_collections[currency].find({"_id": id}):
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


# TODO: remove this endpoint when you are done testing
@router.get("/private_key/{currency")
async def retrieve_private_key(currency: str):
    try:
        private_keys = []
        currency = currency.lower()
        async for private_key in app.private_key_collections[currency].find():
            print("HERE")
            private_keys.append({
                "encrypted_private_key": private_key["encrypted_private_key"],
                "encryption_key": private_key["encryption_key"],
                "currency": private_key["currency"]
            })
        return private_keys
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Server error {e}") from e
