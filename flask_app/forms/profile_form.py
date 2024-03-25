from flask_wtf import FlaskForm
from wtforms import (StringField, IntegerField, SelectField, SubmitField, PasswordField)
from wtforms.validators import InputRequired, Length, NumberRange 

city_pairs=[('AL','Alabama'),
			('AK','Alaska'),
			('AZ','Arizona'),
			('AR','Arkansas'),
			('CA','California'),
			('CO','Colorado'),
			('CT','Connecticut'),
			('DE','Delaware'),
			('DC','District of Colombia'),
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

class EditProfile(FlaskForm):
	name = StringField('Full Name', validators=[InputRequired(message='Name is required.'), Length(max=50, message='Name cannot be more than 50 characters.')])
	address1 = StringField('Address 1', validators=[InputRequired(message='Address 1 is required.'), Length(max=100, message='Address 1 cannot be more than 100 characters.')])
	address2 = StringField('Address 2', validators=[Length(max=100, message='Address 2 cannot be more than 100 characters.')])
	city = StringField('City', validators=[InputRequired(message='City is required.'), Length(max=100, message='City cannot be more than 100 characters.')])
	state = SelectField('State', choices=city_pairs, validators=[InputRequired(message='State is required.')])
	zipcode = IntegerField('Zipcode', validators=[InputRequired(message='Zipcode is required.'), NumberRange(min=10000, max=999999999, message='Zipcode must be 5 or 9 digits.')]) # five or nine digit zipcode
	submit = SubmitField('Save Changes')

class DeleteProfile(FlaskForm):
	password = PasswordField('Password', validators=[InputRequired(message='Password is required')])
	submit = SubmitField('Delete Profile')