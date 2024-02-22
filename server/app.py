from flask import Flask, jsonify,render_template
from flask_cors import CORS
import os

current_dir = os.path.dirname(__file__).strip('\server')+'\client\public'

# template_folder = os.path.join(current_dir, '/public')


# instantiate the app
app = Flask(__name__,template_folder=current_dir)
#Get the absolute path from the folder
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

@app.route('/price')
def priced():
    return render_template('price.html')

if __name__ == '__main__':
    app.run()