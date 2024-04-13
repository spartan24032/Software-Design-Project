import pytest
from app import app  # Import your Flask app instance
from flask import session

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_quote_form_get(client):
    with client.session_transaction() as sess:
        sess['username'] = 'test_user'
    response = client.get('/quote_form')
    assert response.status_code == 200


def test_quote_form_post_valid(client):
    with client.session_transaction() as sess:
        sess['username'] = 'test_user'
    response = client.post('/quote_form', data={'gallons': '100', 'deliveryAddress': '123 Main St', 'deliveryDate': '2024-04-12'})
    assert response.status_code == 200


def test_quote_form_post_invalid(client):
    # Test posting without session
    response = client.post('/quote_form', data={'gallons': '100', 'deliveryAddress': '123 Main St', 'deliveryDate': '2024-04-12'})
    assert response.status_code == 302  # Redirects to login


def test_finalize_value_post(client):
    with client.session_transaction() as sess:
        sess['username'] = 'test_user'
    response = client.post('/finalize_value', data={'totalAmount': '$500', 'suggestedPrice': '$2.50', 'gallons': '100', 'date': '2024-04-12', 'address': '123 Main St'})
    assert response.status_code == 200

