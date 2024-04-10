
from flask import Flask,send_file,jsonify,render_template,request,redirect,session
from werkzeug.datastructures import ImmutableMultiDict
from flask_wtf import FlaskForm
from flask_app import create_app
import os
import random
import config
import hashlib
from flask_app.forms.login_signup import LoginForm, SignupForm
from flask_app.forms.profile_form import EditProfile, DeleteProfile
from flask_app.forms.order_form import QuoteForm

#Imports for the Database 
import pymysql

from PricingModel import Calculation

app = create_app()


f = None
try:
    f = open('vanguard.env', 'r')
except:
    print("vanguard.env not found. Create a new file called coogmusic.env, and put the host, username, password, database in this new file, each separated by line")
    exit(1)

env_lines = f.read().splitlines()

def get_conn():
    return pymysql.connect(
        host=env_lines[0].strip(),
        user=env_lines[1].strip(),
        password=env_lines[2].strip(),
        database=env_lines[3].strip()
    )
def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).digest()    

def check_login(username,password):
    query = 'Select encrypted_password From UserCredentials WHERE username =%s'
    vals = username
    #print(hash_password(password))
    with get_conn() as conn, conn.cursor() as cursor:
        cursor.execute(query, vals)
        result = cursor.fetchone()
        conn.commit()
        if result is None: return False
        return(hash_password(password)==result[0])

users = []

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.name = ""
        self.address1 = ""
        self.address2 = ""
        self.city = ""
        self.state = ""
        self.zipcode = ""
    
    def get_username(self):
        return self.username
    
    def get_password(self):
        return self.password
    def add_profile(self):
        with get_conn() as conn, conn.cursor() as cursor:
            query = 'INSERT INTO UserCredentials (username, encrypted_password)VALUES (%s,%s)'
            vals =(self.username,hash_password(self.password))
            cursor.execute(query,vals)
            conn.commit()
         





def edit_user(name, address1, address2, city, state, zipcode):
    session_user = session.get('username')
    if session_user:
        for user in users:
            if session_user == user.get_username():
                user.name = name
                user.address1 = address1
                user.address2 = address2
                user.city = city
                user.state = state
                user.zipcode = zipcode
                return True
    else:
        return False

def delete_user():
    index = 0
    session_user = session.get('username')
    if session_user:
        for user in users:
            if session_user == user.get_username():
                del users[index]
                return True
            index += 1
    return False

fuel_quotes = [
        {'clientName': 'Sahib Singh', 'clientAddress': '321 bigandtall, Houston, TX', 'gallonsRequested': 5, 'deliveryDate': '2024-01-01', 'pricePerGallon': '3.00', 'totalAmountDue': '$15.00'},
        {'clientName': 'John Doe', 'clientAddress': '123 Elm St, New York, NY', 'gallonsRequested': 10, 'deliveryDate': '2024-01-15', 'pricePerGallon': '2.75', 'totalAmountDue': '$27.50'}
    ]

def add_fuel_quote(fuel_quotes, client_name, client_address, gallons_requested, delivery_date, price_per_gallon, total_amount_due):
    new_quote = {
        'clientName': client_name,
        'clientAddress': client_address,
        'gallonsRequested': gallons_requested,
        'deliveryDate': delivery_date,
        'pricePerGallon': price_per_gallon,
        'totalAmountDue': total_amount_due
    }
    fuel_quotes.append(new_quote)

def non_valid_point():
    if ("username" not in session):
        return True

#Routing Functions 
@app.route('/') 
def homepage():
    return render_template('index.html',image_filename=r'/img/swif.jpg')

#Landing Page for the Order Form 
@app.route('/quote_form',methods=['POST','GET'])
def fuel_quote_form():
    if(non_valid_point()): return render_template('index.html',image_filename=r'/img/swif.jpg')
    formQ = QuoteForm()
    if request.method =="GET":
         return render_template("quote_form.html",form=formQ,fuel_quotes=fuel_quotes)
    if formQ.validate_on_submit():
        gallons, address, date = formQ.gallons.data,formQ.deliveryAddress.data,formQ.deliveryDate.data
        formQ.price.data  = Calculation.Price(gallons,'Texas',False)
        return render_template("quote_form.html",form=formQ,fuel_quotes=fuel_quotes)
    else:
        return render_template("quote_form.html",form=formQ,fuel_quotes=fuel_quotes)


@app.route('/finalize_value',methods=['POST'])
def confirm_quote():
    if(non_valid_point()): return render_template('index.html',image_filename=r'/img/swif.jpg')
    if request.method == "POST":
        data_incoming = request.form
        Total_Amount = data_incoming.get('totalAmount').strip('$')
        Suggested_Price = data_incoming.get('suggestedPrice').strip('$')
        Gallons = data_incoming.get('gallons')
        Date = data_incoming.get('date')
        Address = data_incoming.get('address')
        add_fuel_quote(fuel_quotes, 'New Name', Address, Gallons, Date, Suggested_Price, Total_Amount)

    return 'Success',200



@app.route('/profile', methods=['POST', 'GET'])
def profile():
    if(non_valid_point()): return render_template('index.html',image_filename=r'/img/swif.jpg')
    return render_template('profile.html', edit=EditProfile(), delete=DeleteProfile())


@app.route('/profile/edit', methods=['POST'])
def edit_profile():
    edit = EditProfile() 
    if edit.validate_on_submit(): # checks if it's a post request and validates
        name = edit.name.data
        address1 = edit.address1.data
        address2 = edit.address2.data
        city = edit.city.data
        state = edit.state.data
        zipcode = edit.zipcode.data
        # No database implementation yet
        if edit_user(name, address1, address2, city, state, zipcode):
            return redirect('/profile')
        else: 
            # TODO: add new route for unsuccessful edit
            return redirect('/profile')
    else:
        return render_template('profile.html', edit=edit, delete=DeleteProfile())



@app.route('/profile/delete', methods=['POST'])
def delete_profile():
    delete = DeleteProfile()
    if delete.validate_on_submit(): 
        # No database implementation yet
        if delete_user():
            return redirect('/signup')
        else: # TODO: add new route for unsuccessful deletion
            return redirect('/signup')
    else:
        return render_template('profile.html', edit=EditProfile(), delete=delete)

@app.route('/signup', methods=['POST','GET'])
def sign_up():
    formS = SignupForm() 
    #print(formS.confirm_password)
    if formS.validate_on_submit():
        username = formS.username.data
        password = formS.password.data
        user = User(username, password)
        user.add_profile()
        #users.append(user)
        return render_template('login.html', form=LoginForm())
    else:
        return render_template('signup.html', form=formS)

#add the links to redirect sign in 
@app.route('/login', methods=['POST','GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = request.form['username']
        password = request.form['password']
        # for user in users:
        #     if username == user.get_username() and password == user.get_password():
        #         session["username"] = username
        #         return redirect('/profile')
        if(check_login(username,password)):
            session["username"] = username
            return redirect('/profile')
        return '<h1>No Profile Exist</h1>'
    else:
        return render_template('login.html',form=form)
   
@app.route('/clear_session')
def clear_out():
    del session['username']
    return 'Success',200


@app.route('/styles.css')
def style_css():
    return send_file(os.path.dirname(__file__)+r'flask_app/public/css/styles.css')

if __name__ == '__main__':
    app.run()

