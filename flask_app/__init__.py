import os
from flask import Flask, session
from dotenv import load_dotenv

def create_app():
	# load environment variables from .env file
	load_dotenv()
	project_dir = os.path.dirname(__file__)
	print(project_dir)
	app = Flask(__name__,template_folder = project_dir+r'\templates',static_folder = project_dir+r'\public')
	#CORS(app) 
	# set a config setting from environment variable. look at config.py to see different config settings
	config_type = os.environ.get('CONFIG_TYPE', default='config.ProductionConfig')
	app.config.from_object(config_type) # config with the name in 'CONFIG_TYPE' will be imported
	return app