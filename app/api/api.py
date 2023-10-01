from fastapi import APIRouter
from app.api import addresses

api_router = APIRouter()
api_router.include_router(addresses.router, prefix="/addresses", tags=["addresses"])
