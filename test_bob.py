import os
import pytest
from app32 import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
#1
#All endpoints work

#structure code:
#     response = client.get('/')
#     assert response.status_code == 200
#     assert b"Landing Page" in response.data
    
def test_endpoint(client):
    endpoints ={'/login','/signup'}
    for i in endpoints:
            response = client.get(i)
            assert response.status_code == 200

