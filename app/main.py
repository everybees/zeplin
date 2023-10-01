from fastapi import FastAPI

from api.addresses import router


app = FastAPI()

app.include_router(router, prefix="/addresses", tags=["addresses"])
