
from flask import Flask
from modules import login_blueprint, client_profile_blueprint, fuel_quote_blueprint

app = Flask(__name__)

# Register blueprints
app.register_blueprint(login_blueprint, url_prefix='/login')
app.register_blueprint(client_profile_blueprint, url_prefix='/client')
app.register_blueprint(fuel_quote_blueprint, url_prefix='/quote')

if __name__ == "__main__":
    app.run(debug=True)