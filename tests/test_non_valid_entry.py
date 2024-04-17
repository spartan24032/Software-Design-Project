import pytest 
import os
import pymysql
from flask_app.forms.order_form import QuoteForm
from app import get_all_fuel_quotes_client
from app import add_fuel_quote
from app import non_valid_point
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
def test_get_all_fuel_quotes_client():

    
    # callin function and puttin result in variable
    result = get_all_fuel_quotes_client()

    # Assert that the result is a list
    assert isinstance(result, list)

    # Optionally, assert that each item in the list is a tuple or a list
    for item in result:
        assert isinstance(item, (tuple, list))


def test_add_fuel_quote(conn):
    # Define test data
    client_address = '123 Elm St, New York, NY'
    gallons_requested = 100
    delivery_date = '2024-04-20'  # Example delivery date
    price_per_gallon = 3.50  # Example price per gallon
    total_amount_due = 350.00  # Example total amount due

    # Call the function with the test data
    add_fuel_quote(client_address, gallons_requested, delivery_date, price_per_gallon, total_amount_due)

    # Query the database to verify the added quote
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM FuelQuote WHERE client_address = %s', (client_address,))
        result = cursor.fetchone()

    # Verify that the quote was successfully added to the database
    assert result is not None  # Check if a row was returned from the database
    assert result[1] == gallons_requested  # Check if gallons_requested matches
    assert result[2] == client_address  # Check if client_address matches
    assert result[3].strftime('%Y-%m-%d') == delivery_date  # Check if delivery_date matches
    assert result[4] == price_per_gallon  # Check if price_per_gallon matches
    assert result[5] == total_amount_due  # Check if total_amount_due matches

# test_non_valid_point.py

def test_non_valid_point_session_missing_username(test_client):
    # Mock the session object to simulate 'username' not being present
    with test_client.session_transaction() as session:

        result = non_valid_point(session)

        # Assert that the function returns True when 'username' is not in session
        assert result is True