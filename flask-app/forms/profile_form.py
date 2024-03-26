from flask_wtf import FlaskForm
from wtforms import (StringField, IntegerField, SelectField, SubmitField)
from wtforms.validators import InputRequired, Length, NumberRange 

city_pairs=[('AL','Alabama'),
			('AK','Alaska'),
			('AZ','Arizona'),
			('AR','Arkansas'),
			('CA','California'),
			('CO','Colorado'),
			('CT','Connecticut'),
			('DE','Delaware'),
			('FL','Florida'),
			('GA','Georgia'),
			('HI','Hawaii'),
			('ID','Idaho'),
			('IL','Illinois'),
			('IN','Indiana'),
			('IA','Iowa'),
			('KS','Kansas'),
			('KY','Kentucky'),
			('LA','Louisiana'),
			('ME','Maine'),
			('MD','Maryland'),
			('MA','Massachusetts'),
			('MI','Michigan'),
			('MN','Minnesota'),
			('MS','Mississippi'),
			('MO','Missouri'),
			('MT','Montana'),
			('NE','Nebraska'),
			('NV','Nevada'),
			('NH','New Hampshire'),
			('NJ','New Jersey'),
			('NM','New Mexico'),
			('NY','New York'),
			('NC','North Carolina'),
			('ND','North Dakota'),
			('OH','Ohio'),
			('OK','Oklahoma'),
			('OR','Oregon'),
			('PA','Pennsylvania'),
			('RI','Rhode Island'),
			('SC','South Carolina'),
			('SD','South Dakota'),
			('TN','Tennessee'),
			('TX','Texas'),
			('UT','Utah'),
			('VT','Vermont'),
			('VA','Virginia'),
			('WA','Washington'),
			('WV','West Virginia'),
			('WI','Wisconsin'),
			('WY','Wyoming')]

class ProfileForm(FlaskForm):
	name = StringField('Full Name', validators=[InputRequired(), Length(max=50)])
	address1 = StringField('Address 1', validators=[InputRequired(), Length(max=100)])
	address2 = StringField('Address 2', validators=[Length(max=100)])
	city = StringField('City', validators=[InputRequired(), Length(max=100)])
	state = SelectField('State', choices=city_pairs, validators=[InputRequired()])
	zipcode = IntegerField('Zipcode', validators=[InputRequired(), NumberRange(min=10000, max=999999999)]) # five or nine digit zipcode
	submit = SubmitField('Save Changes')