import pytest
from PricingModel import Calculation

@pytest.fixture
def calculation():
    return Calculation()


#gallons_requested, delivery_state, has_history
def test_price_with_history(calculation):
    price_per_gallon, total_amount_due = calculation.Price(1500, 'TX', True)
    assert price_per_gallon == 1.7
    assert total_amount_due == 2542.5

def test_price_without_history(calculation):
    price_per_gallon, total_amount_due = calculation.Price(800, 'C', False)
    assert price_per_gallon == 1.75
    assert total_amount_due == 1404.0

def test_price_low_gallons(calculation):
    price_per_gallon, total_amount_due = calculation.Price(500, 'TX', True)
    assert price_per_gallon == 1.71
    assert total_amount_due == 855.00

def test_price_high_gallons(calculation):
    price_per_gallon, total_amount_due = calculation.Price(2000, 'TX', True)
    assert price_per_gallon == 1.7
    assert total_amount_due == 3390.0 

def test_price_out_of_texas(calculation):
    price_per_gallon, total_amount_due = calculation.Price(1000, 'C', True)
    assert price_per_gallon == 1.74
    assert total_amount_due == 1740.00

def test_price_out_of_texas_no_history(calculation):
    price_per_gallon, total_amount_due = calculation.Price(1000, 'C', False)
    assert price_per_gallon == 1.75
    assert total_amount_due == 1755.0
