from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, DateField
from wtforms.validators import InputRequired, Length, NumberRange, ValidationError
from datetime import date
class QuoteForm(FlaskForm):
    gallons = IntegerField('Gallons', validators=[InputRequired(), NumberRange(min=1)])
    #deliveryAddress = StringField('Delivery Address', validators=[InputRequired(), Length(min=10, max=100)])
    deliveryDate = DateField('Delivery Date', validators=[InputRequired()])
    submit = SubmitField('Get Quote')
    price = StringField('Price')
    def validate_deliveryDate(self, deliveryDate):
        if deliveryDate.data <= date.today():
            raise ValidationError('Delivery date must be in the future.')
