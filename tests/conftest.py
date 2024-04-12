import pytest
import pymysql
import hashlib
from flask_app import create_app
from app import app
import os

# Define a function to establish the database connection
def get_conn():
    try:
        return pymysql.connect(
            host=os.environ.get('MYSQL_HOST', default='MYSQL_HOST'),
            user=os.environ.get('MYSQL_USER', default='MYSQL_USER'),
            password=os.environ.get('MYSQL_PASSWORD', default='MYSQL_PASSWORD'),
            database=os.environ.get('MYSQL_DB', default='MYSQL_DB')
        )
    except Exception as e:
        print(f"Error occurred while connecting to the database: {e}")
        exit(1)

# This file contains pytest fixtures: helper functions that can be passed to other test functions
def hash_password(password): return hashlib.sha256(password.encode('utf-8')).digest()    

@pytest.fixture(scope="module")
def conn():
    # Establish the database connection
    connection = get_conn()
    yield connection
    # Clean up after testing
    connection.close()

@pytest.fixture(scope="module")
def hash():
    # Provide the hash function
    return hash_password

@pytest.fixture()
def test_client(conn):

    # Configure app for testing
    app.config.from_object('config.TestingConfig')

    # test_client() is a Flask method that makes requests to the application without running a live server. Has methods that mimic HTTP methods like client.get() and client.post()
    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client
