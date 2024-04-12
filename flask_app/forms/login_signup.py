from flask import Flask, render_template, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo,ValidationError
import os

#app = Flask(__name__)
#app.config['SECRET_KEY'] = 'your_secret_key'

import pymysql
def get_conn():
    try:
        return pymysql.connect(
            host=os.environ.get('MYSQL_HOST', default='MYSQL_HOST'),
            user=os.environ.get('MYSQL_USER', default='MYSQL_USER'),
            password=os.environ.get('MYSQL_PASSWORD', default='MYSQL_PASSWORD'),
            database=os.environ.get('MYSQL_DB', default='MYSQL_DB')
        )
    except Exception as e:
        print(f"Error occurred while connecting to the databaseas: {e}")
        exit(1)


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=80)])
    submit = SubmitField('Login')

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=80)])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    def validate_username(self, username ):
        with get_conn() as conn, conn.cursor() as cursor:
            query = 'Select 1 FROM UserCredentials WHERE username = %s'
            vals =(username.data)
            cursor.execute(query,vals)
            login_present = cursor.fetchone()
            conn.commit()
            if(login_present is not None):
                raise ValidationError('This username already has a login!')