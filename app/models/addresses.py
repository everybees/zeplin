from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class CryptoCurrency(str, Enum):
    BTC = "BTC"
    ETH = "ETH"


class Address(BaseModel):
    id: Optional[int]
    address: str
    currency: str
    date_created: Optional[datetime] = None


class PrivateData(BaseModel):
    private_key: str
    key: str
    currency: Optional[str] = None
