import os
from typing import Tuple, Any, Optional

from bit import Key
from cryptography.fernet import Fernet
from eth_keys import keys


def keys_to_dict(private_key: str) -> Tuple[str, str]:
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)
    cipher_text = cipher_suite.encrypt(private_key.encode())

    return cipher_text.decode(), key.decode()


def generate_address_eth() -> Tuple[str, str, Any]:
    private_key = keys.PrivateKey(os.urandom(32))
    public_key = private_key.public_key
    eth_address = public_key.to_checksum_address()
    a, b = keys_to_dict(str(private_key))

    return a, b, eth_address


def generate_address_btc() -> Tuple[str, str, Any]:
    key = Key()
    private_key = key.to_hex()
    public_key = key.public_key
    bitcoin_address = key.address
    a, b = keys_to_dict(str(private_key))

    return a, b, bitcoin_address


def generate_address(currency: str) -> Tuple[Optional[str], Optional[str], Optional[Any]]:
    private_key, encryption_key, address, public_key = None, None, None, None
    if currency == "BTC":
        private_key, encryption_key, address = generate_address_btc()
    elif currency == "ETH":
        private_key, encryption_key, address = generate_address_eth()
    return private_key, encryption_key, address
