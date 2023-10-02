from unittest.mock import patch, MagicMock

import mongomock
import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from datetime import datetime

from app.api.addresses import create_addresses, list_addresses
from app.main import app

from datetime import timezone

client = TestClient(app)


async def mock_get_next_id():
    return 1


def mock_generate_address():
    return "mock_private_key", "mock_encryption_key", "mock_address"


class TestAddresses:

    @pytest.fixture(autouse=True)
    def setup_class(self, mocker):
        self.mocker = mocker
        self.mocked_collection = mocker.MagicMock()
        self.mocker.patch('path.to.your.collection', self.mocked_collection)

        # Mock the data that your functions will return
        self.mock_address_data = {
            "id": 1,
            "address": "mock_address",
            "currency": "BTC",
            "date_created": datetime.now(timezone.utc),
        }

    # Helper function to mock your real function responses

    # Test cases
    @patch("app.api.addresses.db_client", mongomock.MongoClient().get_database("mongo"))
    async def test_create_address(self):
        # Mock the dependent functions and methods
        patch("your_project.routers.addresses.generate_address", side_effect=mock_generate_address)
        patch("your_project.routers.addresses.get_next_id", side_effect=mock_get_next_id)
        patch("your_project.routers.addresses.private_key_collection.insert_one", return_value=None)
        patch("your_project.routers.addresses.currency_collection.insert_one", return_value=None)

        response = client.post("/address/btc")
        assert response.status_code == 200
        assert response.json() == self.mock_address_data

    @patch("app.api.addresses.db_client", mongomock.MongoClient().get_database("mongo"))
    async def test_create_address_invalid_currency(self):
        with pytest.raises(HTTPException):
            await create_addresses("INVALID_CURRENCY")

    @patch("app.api.addresses.db_client", mongomock.MongoClient().get_database("mongo"))
    async def test_create_address_server_error(self):
        # Let’s mock an exception to simulate a server error
        patch("your_project.routers.addresses.generate_address", side_effect=Exception("Mock exception"))

        with pytest.raises(HTTPException) as e:
            await create_addresses("btc")
        assert e.value.status_code == 500
        assert str(e.value.detail) == "Server error"

    @patch("app.api.addresses.db_client", mongomock.MongoClient().get_database("mongo"))
    async def test_list_addresses(self):
        # Mocking the AsyncIOMotorCursor object returned by find method.
        fake_addresses = [
            {
                "address": "some_address",
                "currency": "btc",
                "_id": "some_id",
                "date_created": "some_date"
            }
            # Add more fake address dicts as needed
        ]

        # Arrange: Set up the return_value or side_effect for the find method
        self.mocked_collection.find.return_value = fake_addresses

        # Act: Call the endpoint or function
        response = client.get("/address/")  # adjust as necessary

        # Assert: Check the expected outcomes
        assert response.status_code == 200
        assert response.json() == fake_addresses

    @patch("app.api.addresses.db_client", mongomock.MongoClient().get_database("mongo"))
    async def test_list_addresses_exception(self):
        patch("your_package.router.currency_collection.find", side_effect=Exception("DB Error"))

        with pytest.raises(HTTPException) as exc_info:
            await list_addresses()

        assert exc_info.value.status_code == 500
        assert str(exc_info.value.detail) == "Server error DB Error"
