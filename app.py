
from flask import Flask,send_file,jsonify,render_template,request,redirect,session
from flask_wtf import FlaskForm
import os
import random

from validation.profile_form import ProfileForm
from validation.order_form import QuoteForm


from PricingModel import Calculation

current_dir = os.path.dirname(__file__) # current_dir = os.path.dirname(__file__).strip('\server')
path_current=r"/flask-app"
current_dir += path_current
print(current_dir)

# instantiate the app
app = Flask(__name__,template_folder=current_dir+r'/templates',static_folder =current_dir+r'/public')
app.secret_key = '38hddjch82183y2f00di'
#Get the absolute path from the folder
app.config.from_object(__name__)

users = {}
def random_quote():
    fuel_quotes = [
        {'clientName': 'Sahib Singh', 'clientAddress': '321 bigandtall, Houston, TX', 'gallonsRequested': 5, 'deliveryDate': '2024-01-01', 'pricePerGallon': '3.00', 'totalAmountDue': '$15.00'},
        {'clientName': 'John Doe', 'clientAddress': '123 Elm St, New York, NY', 'gallonsRequested': 10, 'deliveryDate': '2024-01-15', 'pricePerGallon': '2.75', 'totalAmountDue': '$27.50'}
    ]
    return  fuel_quotes


def calculate_price(gallons_requested, delivery_state, has_history):
    current_price_per_gallon = 1.50
    location_factor = 0.02 if 'Texas' in delivery_state else 0.04
    rate_history_factor = 0.01 if has_history else 0
    gallons_requested_factor = 0.02 if gallons_requested > 1000 else 0.03
    company_profit_factor = 0.10
    margin = (location_factor - rate_history_factor + gallons_requested_factor + company_profit_factor) * current_price_per_gallon
    suggested_price_per_gallon = current_price_per_gallon + margin
    total_amount_due = gallons_requested * suggested_price_per_gallon
    return suggested_price_per_gallon, total_amount_due

#Routing Functions 
@app.route('/') 
def homepage():
    return render_template('index.html',image_filename=r'/img/swif.jpg')

#/fuel_quote_form --> Joshua
@app.route('/quote_form',methods=['POST','GET'])
def fuel_quote_form():
    formQ = QuoteForm()
    if request.method =="GET":
         return render_template("quote_form.html",form=formQ,fuel_quotes=random_quote())
    if formQ.validate_on_submit():
        gallons, address, date = formQ.gallons.data,formQ.deliveryAddress.data,formQ.deliveryDate.data
        Price = Calculation.Price(gallons,'Texas',False)
        formQ.price.data =Price
        return render_template("quote_form.html",form=formQ,fuel_quotes=random_quote())
    else:
        return render_template("quote_form.html",form=formQ,fuel_quotes=random_quote())


# profile --> sebastian
@app.route('/profile', methods=['POST', 'GET'])
def profile_mangagement():
    form = ProfileForm() # under the hood, request.form is passed as an argument
    if form.validate_on_submit(): # checks if its a post request and validates
        name = form.name.data
        address1 = form.address1.data
        address2 = form.address2.data
        city = form.city.data
        state = form.state.data
        zipcode = form.zipcode.data
        print(name, address1, address2, city, state, zipcode)
        return render_template('profile.html', form=form)
    else:
        return render_template('profile.html', form=form)


@app.route('/signup', methods=['POST','GET'])
def sign_up():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users[username] = password
        return render_template('login.html')
    elif request.method == 'GET':
        return render_template('signup.html')

#add the links to redirect sign in 
@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username] == password:
            form = ProfileForm()
            return render_template ('profile.html', form=form)
        else:
            return '<h1>invalid credentials!</h1>'
    elif request.method == 'GET':
        return render_template('login.html')

@app.route('/styles.css')
def style_css():
    print(current_dir)
    return send_file(current_dir+r'/public/css/styles.css')

if __name__ == '__main__':
    app.run(debug=1)

