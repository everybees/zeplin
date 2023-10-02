from fastapi import FastAPI

from api.addresses import router
from db.mongodb import startup_db_client, shutdown_db_client

app = FastAPI()


app.include_router(router, prefix="/addresses", tags=["addresses"])

app.add_event_handler("startup", startup_db_client)
app.add_event_handler("shutdown", shutdown_db_client)
