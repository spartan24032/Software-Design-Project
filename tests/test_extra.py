import pytest
from app import app,get_userID,get_clientID
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


def test_finalize_value_post(test_client,conn,hash):
    username ="fuel_quotes"
    password = "secret_secret"
    ph = dict()
    ph['username'] = username

    with conn.cursor() as cursor:
            query = "DELETE FROM UserCredentials WHERE username = %s"
            vals = (username)
            cursor.execute(query, vals)
    conn.commit()

        # Add test user 
    with conn.cursor() as cursor:
            query = "INSERT INTO UserCredentials (username, encrypted_password) VALUES (%s,%s)"
            vals = (username, hash(password))
            cursor.execute(query, vals)
    conn.commit()

        # Set session username
    ID = 0
    with test_client.session_transaction() as sess: 
            sess['username'] = username
            ID = get_userID(sess)

        # Insert test client information
    with conn.cursor() as cursor:
            query = "INSERT INTO ClientInformation (name, address1, address2, city, state, zipcode,user_credentials_id)VALUES (%s,%s,%s,%s,%s,%s,%s) "
            vals = ('EDIT ME','123 I need Edit',"",'EL PASO','TX','77246',ID)
            cursor.execute(query,vals)
    conn.commit()
    response = test_client.post('/finalize_value', data={'totalAmount': '$500', 'suggestedPrice': '$2.50', 'gallons': '100', 'date': '2024-04-12', 'address': '123 Main St'})
    assert response.status_code == 200
def test_clear_out(test_client):
    with test_client.session_transaction() as sess:
        sess['username'] = 'test_user'
    response = test_client.get('/clear_session')
    assert response.status_code == 200
    assert 'username' not in session


def test_clear_out_no_username(test_client):
    response = test_client.get('/clear_session')
    assert response.status_code == 302  # Redirect status code
