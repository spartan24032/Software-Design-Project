from flask import Flask, render_template, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo,ValidationError

#app = Flask(__name__)
#app.config['SECRET_KEY'] = 'your_secret_key'

import pymysql
f = None
try:
    f = open('SQL_INFO.env', 'r')
except:
    print("SQL_INFO.env not found. Create a new file called coogmusic.env, and put the host, username, password, database in this new file, each separated by line")
    exit(1)

env_lines = f.read().splitlines()

def get_conn():
    return pymysql.connect(
        host=env_lines[0].strip(),
        user=env_lines[1].strip(),
        password=env_lines[2].strip(),
        database=env_lines[3].strip()
    )


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
            print(username.data)
            query = 'Select 1 FROM UserCredentials WHERE username = %s'
            vals =(username.data)
            cursor.execute(query,vals)
            login_present = cursor.fetchone()
            conn.commit()
            print(login_present)
            if(login_present is not None):
                raise ValidationError('This username already has a login!')