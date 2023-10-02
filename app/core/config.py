import os
import logging


MONGODB_URL = os.getenv("MONGODB_URL")
DB_NAME = os.getenv("DB_NAME")
CURRENCY_COLLECTION_NAME = os.getenv("CURRENCY_COLLECTION_NAME")
PRIVATE_KEY_COLLECTION_NAME = os.getenv("PRIVATE_KEY_COLLECTION_NAME")
CURRENCIES = {
    "btc": "BTC",
    "eth": "ETH",
}


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
