import pytest
import hashlib
from app import has_history,get_userID,add_fuel_quote,get_clientID


def test_login_get(test_client):
    
    response = test_client.get('/login')
    # Test if get request is successful
    assert response.status_code == 200

def test_signup_get(test_client):
    response = test_client.get('/signup')
    # Test if get request is successful
    assert response.status_code == 200

def test_login(test_client, conn, hash):

    correct_username = 'test_user23'
    correct_password = 'test_pass23'
    incorrect_username = 'test_user33'
    incorrect_password = 'test_pass33'

    # If username exists already in table, delete it first?
    with conn.cursor() as cursor:
        query = "DELETE FROM UserCredentials WHERE username =%s"
        cursor.execute(query,correct_username)
    conn.commit()

    # Test successful login. In order to login, must already have credentials in UserCredentials
    with conn.cursor() as cursor:
        query = "INSERT INTO UserCredentials (username, encrypted_password) VALUES (%s,%s)"
        vals= (correct_username, hash(correct_password))
        cursor.execute(query,vals)
    conn.commit()

    response = test_client.post('/login', 
                                data={'username': correct_username, 'password': hash(correct_password)},
                                follow_redirects=True)
    
    assert response.status_code == 200

    # Test unsuccessful login
    response = test_client.post('/login', 
                                data={'username': incorrect_username, 'password': hash(incorrect_password)},
                                follow_redirects=True)
    
    # If login unsuccessful, should redirect to login
    assert "Go Back" in response.text

def test_sign_up(test_client, conn, hash):

    username = 'test_user23'
    password = 'test_pass23'

    # If username exists already in table, delete it (uniqueness constraint)
    with conn.cursor() as cursor:
        query = "DELETE FROM UserCredentials WHERE username =%s"
        cursor.execute(query,"username")
    conn.commit()

    response = test_client.post('/signup', 
                                data={'username': username, 'encrypted_password': hash(password)})

    # check if sign up inserted new user data
    with conn.cursor() as cursor:
        query = 'SELECT username FROM UserCredentials WHERE username =%s'
        vals = (username)
        cursor.execute(query,vals)
        result = cursor.fetchone()
    conn.commit()
    
    assert result != None

def test_has_history(test_client,conn,hash): 
    username ="history_man"
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
    client_address = '123 Elm St, New York, NY'
    gallons_requested = 100
    delivery_date = '2024-04-20'  # Example delivery date
    price_per_gallon = 3.50  # Example price per gallon
    total_amount_due = 350.00  # Example total amount due

    # Call the function with the test data
    add_fuel_quote(ph,client_address, gallons_requested, delivery_date, price_per_gallon, total_amount_due)

    assert has_history(ph)
    get_history = 'Delete  FROM FuelQuote WHERE client_id = %s'
    with conn.cursor() as cursor:
            cursor.execute(get_history,get_clientID(ph))
            get_history = cursor.fetchall()
            conn.commit()
    assert not has_history(ph)
