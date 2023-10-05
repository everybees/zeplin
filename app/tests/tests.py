import pytest
from fastapi.testclient import TestClient
from mongomock import MongoClient

from core.config import CURRENCIES
from main import app


@pytest.fixture(scope="session")
def client():
    return TestClient(app)


@pytest.fixture(scope="session")
def setup_app():
    app.mongodb_client = MongoClient()
    app.mongodb = app.mongodb_client.get_database('testdb')
    app.currency_collections = {}
    app.private_key_collections = {}

    for currency in CURRENCIES:
        currency_collection_name = f"{currency}-collection"
        private_key_collection_name = f"{currency}-private-key-collection"

        app.currency_collections[currency] = app.mongodb.get_collection(currency_collection_name)
        app.private_key_collections[currency] = app.mongodb.get_collection(private_key_collection_name)

    print("Test Database connected")
    return app


def test_create_addresses(client, setup_app):
    with client:
        response = client.post("/addresses/address/BTC")
        assert response.status_code == 200
        assert response.json()["currency"] == "btc"

        # Test with invalid currency
        response = client.post("/addresses/address/INVALID")
        assert response.status_code == 400


def test_list_addresses(client, setup_app):

    with client:
        # Test with a valid currency
        response = client.get("/addresses/address", params={"currency": "BTC"})
        assert response.status_code == 200

        # Test with an invalid currency
        response = client.get("/addresses/address", params={"currency": "INVALID"})
        assert response.status_code == 200  # As it defaults to listing all currencies

        # Test without currency (lists all addresses of all currencies)
        response = client.get("/addresses/address")
        assert response.status_code == 200


def test_retrieve_address(client, setup_app):

    with client:
        # Test with valid ID and currency
        response = client.get("/addresses/address/BTC/1")
        assert response.status_code == 200

        # Test with invalid ID and valid currency
        response = client.get("/addresses/address/BTC/999999")
        assert response.status_code == 200  # If ID does not exist, it returns an empty list

        # Test with invalid currency
        response = client.get("/addresses/address/INVALID/1")
        assert response.status_code == 500  # As invalid currency results in a server error


def test_retrieve_private_key(client, setup_app):

    with client:
        # Test with valid ID and currency
        response = client.get("/addresses/private_key/BTC")
        assert response.status_code == 200

        # Test with invalid ID and valid currency
        response = client.get("/addresses/private_key/BTC/999999")
        assert response.status_code == 200
