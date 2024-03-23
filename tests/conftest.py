import pytest
import os
from flask_app import create_app # look in __init__.py file for more info
from app import app

# this file contains pytest fixtures: helper functions that can be passed to other test functions

@pytest.fixture()
def test_client():
	
	# configure app for testing. refer to config.py for more info
    app.config.from_object('config.TestingConfig')

    # test_client() is a Flask method that makes requests to the application without running a live server. has methods that mimick HTTP methods like client.get() and client.post()
    with app.test_client() as testing_client:
        """
			The use of 'with' is used for resource management. 
            Use it when you want a resource to be properly closed. 
            Both test_client and app_context() support the use of 'with'. 
            They can be considered as context managers.
        """
        # for more info on app_context(): https://flask.palletsprojects.com/en/2.3.x/appcontext/ 
        with app.app_context():
            """
				Yield is used to return an object like a regular return statement. 
				The difference is that the code after yield will continue executing after the function calling this function (app()) finishes. 
			 	In this instance, it's so that functions calling test_client_app remain in the app_context()
			"""
            yield testing_client