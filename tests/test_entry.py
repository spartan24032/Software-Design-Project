import pytest

def test_login_get(test_client):
    response = test_client.get('/login')
    # Test if get request is successful
    assert response.status_code == 200


def test_signup_get(test_client):
    response = test_client.get('/signup')
    # Test if get request is successful
    assert response.status_code == 200
