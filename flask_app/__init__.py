import os
from flask import Flask, session

project_dir = os.path.dirname(__file__)

def create_app():
	app = Flask(__name__,template_folder = project_dir+r'\templates',static_folder = project_dir+r'\public')
	# set a config setting from environment variable. look at config.py to see different config settings
	config_type = os.environ.get('CONFIG_TYPE', default='config.DevelopmentConfig')
	app.config.from_object(config_type) # config with the name in 'CONFIG_TYPE' will be imported
	print(app.template_folder)#
	return app