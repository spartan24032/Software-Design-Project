import pytest 
from flask_app.forms.order_form import QuoteForm
from datetime import date


def test_fuel_quote_get(test_client):
    """Test the /quote_form route for GET request."""
    response = test_client.get('/quote_form')

    assert response.status_code == 200

def test_fuel_quote_post(test_client):
    """Test the /quote_form route for POST request."""
    data = {
        'gallons': '10',
        'deliveryAddress': '123 Elm St, New York, NY',
        'deliveryDate': '2024-03-30'
    }
    response = test_client.post('/quote_form', data=data)

    assert response.status_code == 200

def test_confirm_quote(test_client):
    """Test the /finalize_value route for POST request."""
    data = {
        'totalAmount': '$100.00',
        'suggestedPrice': '$2.50',
        'gallons': '20',
        'date': '2024-03-30',
        'address': '456 Oak St, Los Angeles, CA'
    }
    response = test_client.post('/finalize_value', data=data)

    assert response.status_code == 200
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
    




