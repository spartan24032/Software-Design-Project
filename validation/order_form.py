from flask_wtf import FlaskForm
from wtforms import (StringField, IntegerField, SelectField, SubmitField,DateField,FloatField)
from wtforms.validators import InputRequired, Length, NumberRange ,ValidationError
from datetime import date


class QuoteForm(FlaskForm):
    gallons = IntegerField('Gallons', validators=[InputRequired(), NumberRange(min=1)])
    deliveryAddress = StringField('Delivery Address', validators=[InputRequired(), Length(min=1, max=100)])
    deliveryDate = DateField('Delivery Date', validators=[InputRequired()])
    def validate_deliveryDate(self, deliveryDate):
        if deliveryDate.data <= date.today():
            raise ValidationError('Delivery date must be after the current date.')
    submit = SubmitField('Get Quote')