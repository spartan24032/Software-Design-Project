
from flask import Flask,send_file,jsonify,render_template,request,redirect,session
from werkzeug.datastructures import ImmutableMultiDict
from flask_wtf import FlaskForm
from flask_app import create_app
import os
import random
import config
from flask_app.forms.login_signup import LoginForm, SignupForm
from flask_app.forms.profile_form import EditProfile, DeleteProfile
from flask_app.forms.order_form import QuoteForm

from PricingModel import Calculation

app = create_app()

# current_dir = os.path.dirname(__file__) # current_dir = os.path.dirname(__file__).strip('\server')
# path_current=r"\flask-app"
# current_dir += path_current

# # instantiate the app
# app = Flask(__name__,template_folder=current_dir+r'/templates',static_folder =current_dir+r'/public')
# app.secret_key = '38hddjch82183y2f00di'
# #Get the absolute path from the folder
# app.config.from_object(__name__)

users = {}
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

#Routing Functions 
@app.route('/') 
def homepage():
    #print(current_dir)
    return render_template('index.html',image_filename=r'/img/swif.jpg')

#Landing Page for the Order Form 
@app.route('/quote_form',methods=['POST','GET'])
def fuel_quote_form():
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
    if request.method == "POST":
        data_incoming = request.form
        Total_Amount = data_incoming.get('totalAmount').strip('$')
        Suggested_Price = data_incoming.get('suggestedPrice').strip('$')
        Gallons = data_incoming.get('gallons')
        Date = data_incoming.get('date')
        Address = data_incoming.get('address')
        add_fuel_quote(fuel_quotes, 'New Name', Address, Gallons, Date, Suggested_Price, Total_Amount)

    return 'Success',200


# profile --> sebastian
@app.route('/profile', methods=['POST', 'GET'])
def profile():
    edit = EditProfile() # under the hood, request.form is passed as an argument
    delete = DeleteProfile()
    return render_template('profile.html', edit=edit, delete=delete)

@app.route('/profile/edit', methods=['POST'])
def edit_profile():
    print('Here')
    edit = EditProfile() 
    if edit.validate_on_submit(): # checks if it's a post request and validates
        name = edit.name.data
        address1 = edit.address1.data
        address2 = edit.address2.data
        city = edit.city.data
        state = edit.state.data
        zipcode = edit.zipcode.data
        # No database implementation yet
        print(name, address1, address2, city, state, zipcode)
        return redirect('/profile')
    else:
        return render_template('profile.html', edit=edit, delete=DeleteProfile())

# profile --> sebastian
@app.route('/profile/delete', methods=['POST'])
def delete_profile():
    delete = DeleteProfile()
    if delete.validate_on_submit(): 
        password = delete.password.data
        # No database implementation yet
        print(password)
        return redirect('/signup')
    else:
        return render_template('profile.html', edit=EditProfile(), delete=delete)
# @app.route('/signup', methods=['POST','GET'])
# def sign_up():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         users[username] = password
#         return render_template('login.html')
#     elif request.method == 'GET':
#         return render_template('signup.html')
@app.route('/signup', methods=['POST','GET'])
def sign_up():
    formS = SignupForm() 
    #print(formS.confirm_password)
    if formS.validate_on_submit():
        username = formS.username.data
        password = formS.password.data
        users[username] = password
        print(3)
        return render_template('login.html', form=LoginForm())
    else:
        print(2)
        return render_template('signup.html', form=formS)

#add the links to redirect sign in 
@app.route('/login', methods=['POST','GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username] == password:
            edit = EditProfile()
            delete = DeleteProfile()
            return render_template ('profile.html', edit=edit, delete=delete)
        else:
            return '<h1>invalid credentials!</h1>'
    else:
        return render_template('login.html',form=form)

@app.route('/styles.css')
def style_css():
    return send_file(os.path.dirname(__file__)+r'flask_app/public/css/styles.css')

if __name__ == '__main__':
    app.run()

