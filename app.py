
from flask import Flask,send_file,jsonify,render_template,request,redirect,session
from flask_wtf import FlaskForm
import os
import random

from validation.profile_form import ProfileForm
from validation.order_form import QuoteForm

current_dir = os.path.dirname(__file__) # current_dir = os.path.dirname(__file__).strip('\server')
path_current=r"/flask-app"
current_dir += path_current
print(current_dir)

# instantiate the app
app = Flask(__name__,template_folder=current_dir+r'/templates',static_folder =current_dir+r'/public')
app.secret_key = '38hddjch82183y2f00di'
#Get the absolute path from the folder
app.config.from_object(__name__)

#Create some logins:

#Functions to generate code/variable setting (no Database employed)
users = {}
def random_quotes():
    random.seed(5)
    client_names = ['Sahib Singh', 'Joshua Mathews', 'Alice Johnson', 'Bob Smith', 'Emma Davis']
    client_addresses = ['321 bigandtall, Houston, TX', '123 tenmilehike, Houston, TX', '456 oakstreet, Dallas, TX', '789 mapleave, Austin, TX', '555 pineboulevard, San Francisco, CA']
    delivery_dates = ['2024-01-01', '2024-02-10', '2024-03-15', '2024-04-20', '2024-05-25']

    # Generate 10 random fuel quotes
    fuel_quotes = []
    for _ in range(10):
        quote = {
            'clientName': random.choice(client_names),
            'clientAddress': random.choice(client_addresses),
            'gallonsRequested': random.randint(1, 1000),
            'deliveryDate': random.choice(delivery_dates),
            'pricePerGallon': '${:.2f}'.format(random.uniform(2.50, 3.00)),  # Random price between $2.50 and $3.00
        }
        # Calculate total amount due
        quote['totalAmountDue'] = '${:.2f}'.format(quote['gallonsRequested'] * float(quote['pricePerGallon'][1:]))
        fuel_quotes.append(quote)
    return fuel_quotes

#Pricing Module 
def calculate_price(gallons_requested, delivery_state, has_history):
    # Constants
    current_price_per_gallon = 1.50
    location_factor = 0.02 if 'Texas' in delivery_state else 0.04
    rate_history_factor = 0.01 if has_history else 0
    gallons_requested_factor = 0.02 if gallons_requested > 1000 else 0.03
    company_profit_factor = 0.10
    
    # Calculate margin
    margin = (location_factor - rate_history_factor + gallons_requested_factor + company_profit_factor) * current_price_per_gallon
    
    # Calculate suggested price per gallon
    suggested_price_per_gallon = current_price_per_gallon + margin
    
    # Calculate total amount due
    total_amount_due = gallons_requested * suggested_price_per_gallon
    
    return suggested_price_per_gallon, total_amount_due

#Routing Functions 
@app.route('/') 
def homepage():
    return render_template('index.html',image_filename=r'/img/swif.jpg')

@app.route('/process_quote', methods=['POST'])
def process_quote():
    print(request.form)
    # Extract data from the request
    gallons_requested = int(request.form['gallonsRequested'])
    delivery_state = request.form['deliveryAddress']
    has_history = True
    suggested_price_per_gallon, total_amount_due = calculate_price(gallons_requested, delivery_state, has_history)
    return jsonify({'suggestedPrice': suggested_price_per_gallon, 'totalAmountDue': total_amount_due})

@app.route('/submit_quote', methods=['POST'])
def submit_quote():
    data = request.get_json()
    print(data)
    gallons_requested = int(data['gallonsRequested'])
    delivery_state = data['deliveryAddress']
    delivery_date = data['deliveryDate']
    has_history = True
    price = calculate_price(gallons_requested, delivery_state, has_history)
    return jsonify({'message': 'Quote submitted successfully'}), 200

#fuel_quote_history --> Sahib

@app.route('/get_history')
def fuel_quote_history():
    #No database implementation yet
    return render_template('fuel_history.html', fuel_quotes=random_quotes())

#/fuel_quote_form --> Joshua
@app.route('/quote_form',methods=['POST','GET'])
def fuel_quote_form():
    formQ = QuoteForm()
    if formQ.validate_on_submit():
        gallons, address, date = formQ.gallons.data,formQ.deliveryAddress.data,formQ.deliveryDate.data
        print(gallons,address,date)
        return render_template("quote_form.html",form=formQ,fuel_quotes=random_quotes())
    else:
        return render_template("quote_form.html",form=formQ,fuel_quotes=random_quotes())


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

