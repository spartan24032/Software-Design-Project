class Calculation:
    def __init__(self) -> None:
        pass
        
    def Price(gallons_requested, delivery_state, has_history):
        current_price_per_gallon = 1.50
        location_factor = 0.02 if 'Texas' in delivery_state else 0.04
        rate_history_factor = 0.01 if has_history else 0
        gallons_requested_factor = 0.02 if gallons_requested > 1000 else 0.03
        company_profit_factor = 0.10
        margin = (location_factor - rate_history_factor + gallons_requested_factor + company_profit_factor) * current_price_per_gallon
        suggested_price_per_gallon = current_price_per_gallon + margin
        total_amount_due = gallons_requested * suggested_price_per_gallon
        return round(suggested_price_per_gallon,2), round(total_amount_due,2)