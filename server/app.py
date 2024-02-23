
from flask import Flask, jsonify,render_template
from flask_cors import CORS
import os

current_dir = os.path.dirname(__file__).strip('\server')
path_current='\client'
current_dir +=path_current



# instantiate the app
app = Flask(__name__,template_folder=current_dir+r'\templates',static_folder =current_dir+r'\public')
#Get the absolute path from the folder
app.config.from_object(__name__)



@app.route('/')
def homepage():
    return render_template('index.html',image_filename='swif.jpg')

#/fuel_quote_form --> Joshua
@app.route('/fuel_quote_form')
def fuel_quote_form():
    return render_template('quote_form.html')

#fuel_quote_history --> Sahib
@app.route('/fuel_quote_history')
def fuel_quote_history():
    return render_template('fuel_history.html')
#
@app.route('/client_profile_management')
def profile_management():
    return render_template('profile.html')

#Login + Sign Up --> Vayeshnavi
@app.route('/login')
def loggin():
    return render_template('login.html')

@app.route('/signup')
def sign_up():
    return render_template('signup.html')

if __name__ == '__main__':
    app.run()

