
from flask import Flask,send_file,jsonify,render_template,request,redirect,session,flash
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

def get_conn():
    try:
        return pymysql.connect(
            host=os.environ.get('MYSQL_HOST', default='MYSQL_HOST'),
            user=os.environ.get('MYSQL_USER', default='MYSQL_USER'),
            password=os.environ.get('MYSQL_PASSWORD', default='MYSQL_PASSWORD'),
            database=os.environ.get('MYSQL_DB', default='MYSQL_DB')
        )
    except Exception as e:
        print(f"Error occurred while connecting to the database_main: {e}")
        exit(1)

#Hash Passwords Into the Database
def hash_password(password): return hashlib.sha256(password.encode('utf-8')).digest()    

def check_login(username,password):
    query = 'SELECT encrypted_password FROM UserCredentials WHERE username =%s'
    vals = username
    #print(hash_password(password))
    with get_conn() as conn, conn.cursor() as cursor:
        cursor.execute(query, vals)
        result = cursor.fetchone()
        conn.commit()
        if result is None: return False
        return(hash_password(password)==result[0])

def get_userID(session ):
    get_user_id  = 'Select ID FROM UserCredentials WHERE username = %s'
    with get_conn() as conn, conn.cursor() as cursor:
            #First Find the ID
            vals =(session['username'])
            cursor.execute(get_user_id,vals)
            get_user_id= cursor.fetchone()
    
            conn.commit()
    return get_user_id[0]
def get_clientID(session):
    get_client_id  = 'Select client_id FROM ClientInformation WHERE user_credentials_id = %s'
    with get_conn() as conn, conn.cursor() as cursor:
            cursor.execute(get_client_id,get_userID(session))
            get_client_id = cursor.fetchone()
            conn.commit()

    if(get_client_id is not None):
        return get_client_id[0] 
    return get_client_id
def get_address(session):
    get_client_address = 'Select address1,city,state,zipcode FROM ClientInformation WHERE user_credentials_id = %s'
    with get_conn() as conn, conn.cursor() as cursor:
            cursor.execute(get_client_address ,get_userID(session))
            get_client_address = cursor.fetchone()
            conn.commit()

    if(get_client_address  is not None):
        get_client_address = get_client_address[0]+ " "+ get_client_address[1] + " "+  get_client_address[2] + " "+  str(get_client_address[3])
        return get_client_address 
    return get_client_address 
def has_history(session):
    get_history = 'Select 1 FROM FuelQuote WHERE client_id = %s'
    with get_conn() as conn, conn.cursor() as cursor:
            cursor.execute(get_history,get_clientID(session))
            get_history = cursor.fetchone()
            conn.commit()
    if(get_history is None):
        return False
    return True
    


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
    if(get_clientID(session) ==None):
        with get_conn() as conn, conn.cursor() as cursor:
            query = "INSERT INTO ClientInformation (name, address1, address2, city, state, zipcode,user_credentials_id)VALUES (%s,%s,%s,%s,%s,%s,%s) "
            vals = (name,address1,address2,city,state,zipcode,get_userID(session))
            cursor.execute(query,vals)
            conn.commit()
        return
    with get_conn() as conn, conn.cursor() as cursor:
        query = """
        UPDATE ClientInformation 
        SET 
            name = %s, 
            address1 = %s, 
            address2 = %s, 
            city = %s, 
            state = %s, 
            zipcode = %s
        WHERE 
            user_credentials_id = %s
    """
        vals = (name, address1, address2, city, state, zipcode, get_userID(session))
        cursor.execute(query, vals)
        conn.commit()



def delete_user(session):
    with get_conn() as conn, conn.cursor() as cursor:
            query = 'DELETE FROM UserCredentials WHERE username = %s'
            vals =(session['username'])
            cursor.execute(query,vals)
            conn.commit()
    del session['username']
    return True
    index = 0
    session_user = session.get('username')
    if session_user:
        for user in users:
            if session_user == user.get_username():
                del users[index]
                return True
            index += 1
    return False


def get_all_fuel_quotes_client(session):
    get_history = 'Select * FROM FuelQuote WHERE client_id = %s'
    with get_conn() as conn, conn.cursor() as cursor:
            cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
            cursor.execute(get_history,get_clientID(session))
            get_history = cursor.fetchall()
            conn.commit()
    #print(get_history)
    return get_history


def add_fuel_quote( session,client_address, gallons_requested, delivery_date, price_per_gallon, total_amount_due):
    insert_quote= 'INSERT INTO FuelQuote (client_id,gallons_requested, delivery_address,delivery_date,suggested_price_per_gallon,total_amount_due)VALUES (%s,%s,%s,%s,%s,%s)'
    with get_conn() as conn, conn.cursor() as cursor:
            vals =(get_clientID(session),gallons_requested,client_address,delivery_date,price_per_gallon,total_amount_due)
            cursor.execute(insert_quote,vals)
            conn.commit()

def get_profile_data():
    place_holder_start = {'name': '','address1': '','address2': '','city': '','state': '','zipcode': ''}

    get_client_info = 'Select name, address1, address2,city,state, zipcode FROM ClientInformation WHERE user_credentials_id = %s'
    with get_conn() as conn, conn.cursor() as cursor:
            #Use this when you need to send data back as a Dictionary instead of a tuple
            cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

            cursor.execute(get_client_info,get_userID(session))
            get_client_info = cursor.fetchone()
            conn.commit()

    if(get_client_info ==None):
        return place_holder_start

    return get_client_info
def non_valid_point(session):
    if ("username" not in session):
        return True

#Routing Functions 
@app.route('/') 
def homepage():
    return render_template('index.html',image_filename=r'/img/swif.jpg')

#Landing Page for the Order Form 
@app.route('/quote_form',methods=['POST','GET'])
def fuel_quote_form():
    if(non_valid_point(session)): return redirect('/')
    if(get_clientID(session)==None): 
        return render_template('error_message.html',error_message ="Please complete profile first.",image_filename=r'/img/broken.jpg')
    formQ = QuoteForm()
    client= {}
    client['deliveryAddress'] = get_address(session)
    if request.method =="GET":
         return render_template("quote_form.html",form=formQ,fuel_quotes=get_all_fuel_quotes_client(session),client=client)
    if formQ.validate_on_submit():
        #print(get_address(session))
        gallons, address= formQ.gallons.data,get_address(session)
        #print(address)
        # Assuming 'gallons', 'address', and 'has_history()' are defined somewhere
        calculation_instance = Calculation()
        #print(has_history())
        session['gallons_requested'] = gallons

    

        formQ.price.data  = calculation_instance.Price(gallons, address, has_history(session))
        return render_template("quote_form.html",form=formQ,fuel_quotes=get_all_fuel_quotes_client(session),client=client)
    else:
        return render_template("quote_form.html",form=formQ,fuel_quotes=get_all_fuel_quotes_client(session),client=client)


@app.route('/finalize_value',methods=['POST'])
def confirm_quote():
    if(non_valid_point(session)): return redirect('/')
    if request.method == "POST":
        data_incoming = request.form
        Total_Amount = data_incoming.get('totalAmount').strip('$')
        Suggested_Price = data_incoming.get('suggestedPrice').strip('$')
        Gallons = 0
        Date = data_incoming.get('date')
        try:
            Gallons = session['gallons_requested'] #data_incoming.get('gallons')
        except KeyError: 
            Gallons = data_incoming.get('gallons')
        Address = get_address(session)
        add_fuel_quote( session,Address, Gallons, Date, Suggested_Price, Total_Amount)

    return 'Success',200



@app.route('/profile', methods=['POST', 'GET'])
def profile():
    if non_valid_point(session): 
        return redirect('/')
    else:
        return render_template('profile.html',profile_data=get_profile_data(),edit=EditProfile(), delete=DeleteProfile())


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
        edit_user(name, address1, address2, city, state, zipcode)
        flash('Profile successfully updated!', 'confirm')
        return render_template("profile.html",profile_data=get_profile_data(), edit=edit, delete=DeleteProfile())
    else:
        flash('Form has invalid input(s)!', 'error')
        return render_template("profile.html",profile_data=get_profile_data(), edit=edit, delete=DeleteProfile())


@app.route('/profile/delete', methods=['POST'])
def delete_profile():
    delete = DeleteProfile()
    if delete.validate_on_submit(): 
        delete_user(session)
        flash('Deletion was successful!', 'confirm')
        return render_template('index.html',image_filename=r'/img/swif.jpg')
    else:
        flash('Password did not match with our database!', 'error')
        return render_template("profile.html",profile_data=get_profile_data(), edit=EditProfile(), delete=delete)

@app.route('/signup', methods=['POST','GET'])
def sign_up():
    if('username' in session):
        return redirect('/profile')
    formS = SignupForm() 
    #print(formS.confirm_password)
    if formS.validate_on_submit():
        username = formS.username.data
        password = formS.password.data
        user = User(username, password)
        user.add_profile()
        return render_template('login.html', form=LoginForm())
    else:
        return render_template('signup.html', form=formS)

#add the links to redirect sign in 
@app.route('/login', methods=['POST','GET'])
def login():
    if('username' in session):
        return redirect('/profile')
    form = LoginForm()
    if form.validate_on_submit():
        username = request.form['username']
        password = request.form['password']
        if(check_login(username,password)):
            session["username"] = username
            return redirect('/profile')
        return render_template('error_message.html',error_message ="This account may not exist. Verify login.",image_filename=r'/img/broken.jpg')
    else:
        return render_template('login.html',form=form)
   
@app.route('/clear_session')
def clear_out():
    if('username' not in session): 
        return redirect('/')
    del session['username']
    return 'Success',200


@app.route('/styles.css')
def style_css():
    return send_file(os.path.dirname(__file__)+r'flask_app/public/css/styles.css')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)),debug=True)

