import os
from typing import Tuple, Any, Optional

from bit import Key
from cryptography.fernet import Fernet
from eth_keys import keys

from core.config import logger


def keys_to_dict(private_key: str) -> Tuple[str, str]:
    try:
        key = Fernet.generate_key()
        cipher_suite = Fernet(key)
        cipher_text = cipher_suite.encrypt(private_key.encode())
        return cipher_text.decode(), key.decode()
    except Exception as e:
        logger.error(f"Error in keys_to_dict: {e}")
        raise e


def generate_address_eth() -> Tuple[str, str, Any]:
    try:
        private_key = keys.PrivateKey(os.urandom(32))
        public_key = private_key.public_key
        eth_address = public_key.to_checksum_address()
        cipher, private_key = keys_to_dict(str(private_key))
        logger.info("Ethereum address generated successfully")
        return cipher, private_key, eth_address
    except Exception as e:
        logger.error(f"Error generating Ethereum address: {e}")
        raise e


def generate_address_btc() -> Tuple[str, str, Any]:
    try:
        key = Key()
        private_key = key.to_hex()
        public_key = key.public_key
        bitcoin_address = key.address
        cipher, private_key = keys_to_dict(str(private_key))
        logger.info("Bitcoin address generated successfully")
        return cipher, private_key, bitcoin_address
    except Exception as e:
        logger.error(f"Error generating Bitcoin address: {e}")
        raise e


def generate_address(currency: str) -> Tuple[Optional[str], Optional[str], Optional[Any]]:
    try:
        private_key, encryption_key, address, public_key = None, None, None, None
        if currency == "btc":
            private_key, encryption_key, address = generate_address_btc()
        elif currency == "eth":
            private_key, encryption_key, address = generate_address_eth()
        logger.info(f"{currency.upper()} address generated successfully")
        return private_key, encryption_key, address
    except Exception as e:
        logger.error(f"Error in generate_address for {currency}: {e}")
        raise e
