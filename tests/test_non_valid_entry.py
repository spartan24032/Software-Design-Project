import pytest 
import os
import pymysql
from flask_app.forms.order_form import QuoteForm
from app import get_all_fuel_quotes_client
from app import add_fuel_quote
from app import non_valid_point,get_userID,get_clientID
from datetime import date







def test_deliveryDate_future_date(test_client):
        form = QuoteForm(deliveryDate=date.today())
        assert not form.validate()

def test_quoteForm_invalid_data(test_client):
        form = QuoteForm(
            gallons=0,  # Invalid gallons value
            deliveryAddress='123 Elm St, New York, NY',
            deliveryDate=date.today()  # Today's date (invalid)
        )
        assert not form.validate()

        form = QuoteForm(
            gallons=5,
            deliveryAddress='Short',  # Invalid deliveryAddress (too short)
            deliveryDate=date.today().replace(year=date.today().year - 1)  # Past date (invalid)
        )
        assert not form.validate()
    

# Define a test case for get_all_fuel_quotes_client
def test_get_all_fuel_quotes_client(test_client,conn,hash):

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

    

    with conn.cursor() as cursor:
            insert_quote= 'INSERT INTO FuelQuote (client_id,gallons_requested, delivery_address,delivery_date,suggested_price_per_gallon,total_amount_due)VALUES (%s,%s,%s,%s,%s,%s)'
            vals =(get_clientID(ph),1,'Blank','2024-04-19','1','1')
            cursor.execute(insert_quote,vals)
            conn.commit()
    conn.commit()



        
        # callin function and puttin result in variable
    result =0
    with test_client.session_transaction() as sess:
        sess['username'] = "fuel_quotes"
        result = get_all_fuel_quotes_client(sess)

        # Assert that the result is a list
    #print(result)
    assert isinstance(result, list)

    for item in result:
            assert isinstance(item, (tuple, dict))


def test_add_fuel_quote(test_client,conn):
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
    # Define test data
    client_address = '123 Elm St, New York, NY'
    gallons_requested = 100
    delivery_date = '2024-04-20'  # Example delivery date
    price_per_gallon = 3.50  # Example price per gallon
    total_amount_due = 350.00  # Example total amount due

    # Call the function with the test data
    add_fuel_quote(ph,client_address, gallons_requested, delivery_date, price_per_gallon, total_amount_due)

    # Query the database to verify the added quote
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM FuelQuote WHERE delivery_address = %s', (client_address,))
        result = cursor.fetchone()
   # print(result)
    # Verify that the quote was successfully added to the database
    assert result is not None  # Check if a row was returned from the database
    assert result[2] == gallons_requested  # Check if gallons_requested matches
    assert result[3] == client_address  # Check if client_address matches
    assert result[4].strftime('%Y-%m-%d') == delivery_date  # Check if delivery_date matches
    assert result[5] == price_per_gallon  # Check if price_per_gallon matches
    assert result[6] == total_amount_due  # Check if total_amount_due matches

# test_non_valid_point.py

def test_non_valid_point_session_missing_username(test_client):
    # Mock the session object to simulate 'username' not being present
    with test_client.session_transaction() as session:

        result = non_valid_point(session)

        # Assert that the function returns True when 'username' is not in session
        assert result is True