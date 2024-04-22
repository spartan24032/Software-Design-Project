import pytest
from flask_app.forms.profile_form import EditProfile, DeleteProfile
from flask import url_for,session
from app import get_userID

    
def test_profile_get(test_client):
	response = test_client.get('/profile')
	assert response.status_code == 302

def test_valid_profile_edit(test_client,conn):
	username = "EDIT_him"
	password = "secret_secret"

	# Remove possible duplicate
	with conn.cursor() as cursor:
		query = "DELETE FROM UserCredentials WHERE username = %s"
		vals = (username)
		cursor.execute(query, vals)
	conn.commit()

	# Add test user 
	with conn.cursor() as cursor:
		query = "INSERT INTO UserCredentials (username, encrypted_password) VALUES (%s,%s)"
		vals = (username, hash(password))
		cursor.execute(query, vals)
	conn.commit()

	# Set session username
	ID = 0
	with test_client.session_transaction() as sess: 
		sess['username'] = username
		ID = get_userID(sess)

	# Insert test client information
	with conn.cursor() as cursor:
		query = "INSERT INTO ClientInformation (name, address1, address2, city, state, zipcode,user_credentials_id)VALUES (%s,%s,%s,%s,%s,%s,%s) "
		vals = ('EDIT ME','123 I need Edit',"",'EL PASO','TX','77246',ID)
		cursor.execute(query,vals)
	conn.commit()
	
	edit_name = 'President'
	edit_address1 = '1600 Pennsylvania Avenue, N.W.'
	edit_address2 = 'Not Applicable'
	edit_city = 'Washington'
	edit_state = 'DC'
	edit_zipcode = '20500'

	# Test with valid data
	response = test_client.post(
		'/profile/edit',
		data={'name': edit_name, 'address1': edit_address1, 'address2': edit_address2, 'city': edit_city, 'state': edit_state, 'zipcode': edit_zipcode},
		follow_redirects=True
	)

	assert response.status_code == 200

	# Check that the database was updated
	with conn.cursor() as cursor:
		query = "SELECT name, address1, address2, city, state, zipcode, user_credentials_id FROM ClientInformation WHERE user_credentials_id = %s"
		vals = (ID)
		cursor.execute(query,vals)
		client_info = cursor.fetchone() # returns a tuple
	conn.commit()

	assert client_info[0] == edit_name
	assert client_info[1] == edit_address1
	assert client_info[2] == edit_address2
	assert client_info[3] == edit_city
	assert client_info[4] == edit_state
	assert client_info[5] == int(edit_zipcode)

	# Teardown
	with conn.cursor() as cursor:
		query = "DELETE FROM ClientInformation WHERE user_credentials_id = %s"
		vals = (ID)
		cursor.execute(query,vals)
	conn.commit()

	with conn.cursor() as cursor:
		query = "DELETE FROM UserCredentials WHERE username = %s"
		vals = (username)
		cursor.execute(query, vals)
	conn.commit()

def test_invalid_profile_edit(test_client, conn):
	name = 'x' * 51 # Name cannot be more than 50 characters.
	address1 = 'x' * 101 # Address 1 cannot be more than 100 characters.
	address2 = 'x' * 101 # Address 2 cannot be more than 100 characters.
	city = 'x' * 101 # City cannot be more than 100 characters.
	state = '' # Can't be empty
	zipcode = 'x' * 1 # Zipcode must be 5 or 9 digits.
	form = EditProfile(name=name, address1=address1, address2=address2, city=city, state=state, zipcode=zipcode)
	assert not form.validate()


def test_valid_profile_deletion(test_client,conn,hash):
	username = "Delete_him"
	password = "secret_secret"

	# Remove possible duplicate
	with conn.cursor() as cursor:
		query = "DELETE FROM UserCredentials WHERE username = %s"
		vals = (username)
		cursor.execute(query, vals)
	conn.commit()

	# Add test user 
	with conn.cursor() as cursor:
		query = "INSERT INTO UserCredentials (username, encrypted_password) VALUES (%s,%s)"
		vals = (username, hash(password))
		cursor.execute(query, vals)
	conn.commit()

	# Set session username
	with test_client.session_transaction() as s:
		s['username'] =username

	# Test with valid password
	response = test_client.post(
			'/profile/delete',
			method = 'POST', 
			data={'password': password},
			follow_redirects=True
		)
	
	assert response.status_code == 200
	
	# Test if deleted 
	with conn.cursor() as cursor:
		query = "SELECT * FROM UserCredentials WHERE username = %s"
		vals = (username)
		cursor.execute(query, vals)
		row = cursor.fetchone()
	conn.commit()

	# If there is no row fetched by the query, it means deletion was successful
	assert row == None

def test_invalid_profile_deletion(test_client, conn):
	password = ''
	form = DeleteProfile(password=password)
	assert not form.validate()