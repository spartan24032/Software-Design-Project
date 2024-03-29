from app import add_fuel_quote
import pytest

def test_index_get(test_client):
    response = test_client.get('/')
    # Test if get request is successful
    assert response.status_code == 200
