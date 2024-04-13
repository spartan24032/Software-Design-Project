import pytest 
from flask_app.forms.order_form import QuoteForm
from datetime import date


def test_fuel_quote_get(test_client):
    
    response = test_client.get('/quote_form')

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
    




