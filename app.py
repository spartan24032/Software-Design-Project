
from flask import Flask,send_file,jsonify,render_template
import os

current_dir = os.path.dirname(__file__) # current_dir = os.path.dirname(__file__).strip('\server')
path_current=r"/flask-app"
current_dir += path_current
print(current_dir)



# instantiate the app
app = Flask(__name__,template_folder=current_dir+r'/templates',static_folder =current_dir+r'/public')
#Get the absolute path from the folder
app.config.from_object(__name__)



@app.route('/')
def homepage():
    return render_template('index.html',image_filename=r'/img/swif.jpg')

#/fuel_quote_form --> Joshua
@app.route('/quote_form')
def fuel_quote_form():
    print(current_dir)
    return render_template('quote_form.html')

#fuel_quote_history --> Sahib
@app.route('/fuel_history')
def fuel_quote_history():
    return render_template('fuel_history.html')
#
@app.route('/profile')
def profile_management():
    return render_template('profile.html')

#Login + Sign Up --> Va is h navi
@app.route('/login')
def loggin():
    return render_template('login.html')

@app.route('/signup')
def sign_up():
    return render_template('signup.html')

@app.route('/styles.css')
def style_css():
    print(current_dir)
    return send_file(current_dir+r'/public/css/styles.css')

if __name__ == '__main__':
    app.run(host ='0.0.0.0' )

