import pytest
from fastapi.testclient import TestClient
from mongomock import MongoClient

from main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def mock_db():
    client = MongoClient()
    db = client.db
    db.btc_collection = client.db.btc_collection
    db.eth_collection = client.db.eth_collection
    yield db
    client.close()


def test_create_addresses(client):
    app.mongodb_client = mock_db
    app.currency_collections = {"btc": mock_db.btc_collection, "eth": mock_db.eth_collection}

    with TestClient(app) as client:
        response = client.post("/address/BTC")
        print(response.json(), "=====================")
        assert response.status_code == 200
        assert response.json()["currency"] == "btc"

        # Test with invalid currency
        response = client.post("/address/INVALID")
        assert response.status_code == 400


def test_list_addresses(client):
    app.mongodb_client = mock_db
    app.currency_collections = {"btc": mock_db.btc_collection, "eth": mock_db.eth_collection}

    with TestClient(app) as client:
        # Test with a valid currency
        response = client.get("/address", params={"currency": "BTC"})
        assert response.status_code == 200

        # Test with an invalid currency
        response = client.get("/address", params={"currency": "INVALID"})
        assert response.status_code == 200  # As it defaults to listing all currencies

        # Test without currency (lists all addresses of all currencies)
        response = client.get("/address")
        assert response.status_code == 200


def test_retrieve_address(client):
    app.mongodb_client = mock_db
    app.currency_collections = {"btc": mock_db.btc_collection, "eth": mock_db.eth_collection}

    with TestClient(app) as client:
        # Test with valid ID and currency
        response = client.get("/address/BTC/1")
        assert response.status_code == 200

        # Test with invalid ID and valid currency
        response = client.get("/address/BTC/999999")
        assert response.status_code == 200  # If ID does not exist, it returns an empty list

        # Test with invalid currency
        response = client.get("/address/INVALID/1")
        assert response.status_code == 500  # As invalid currency results in a server error


def test_retrieve_private_key(client):
    app.mongodb_client = mock_db
    app.currency_collections = {"btc": mock_db.btc_collection, "eth": mock_db.eth_collection}

    with TestClient(app) as client:
        # Test with valid ID and currency
        response = client.get("/private_key/BTC/1")
        assert response.status_code == 200

        # Test with invalid ID and valid currency
        response = client.get("/private_key/BTC/999999")
        assert response.status_code == 200
