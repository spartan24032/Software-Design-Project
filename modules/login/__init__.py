from .login_blueprint import login_blueprint

# Example route inside login_blueprint.py

from flask import render_template

@login_blueprint.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')
