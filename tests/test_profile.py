import pytest
from flask_app.forms.profile_form import EditProfile, DeleteProfile
from flask import url_for,session
from app import get_userID

    
def test_profile_get(test_client):
	response = test_client.get('/profile')
	# Test if get request is successful
	print(response.data)
	assert response.status_code == 302

def test_edit_profile(test_client,conn):
	username ="EDIT_him"
	password = "secret_secret"
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
	ID = 0
	with test_client.session_transaction() as sess: 
		sess['username'] = username
		ID = get_userID(sess)

	with conn.cursor() as cursor:
		query = "INSERT INTO ClientInformation (name, address1, address2, city, state, zipcode,user_credentials_id)VALUES (%s,%s,%s,%s,%s,%s,%s) "
		vals = ('EDIT ME','123 I need Edit',"",'EL PASO','TX','77246',ID)
		cursor.execute(query,vals)
	conn.commit()
	# Test with valid form data. Populating the form fields by passing in a dictionary to 'data'.
	
	response = test_client.post(
		'/profile/edit',
		data={'name': 'President', 'address1': '1600 Pennsylvania Avenue, N.W.', 'address2': 'Not Applicable', 'city': 'Washington', 'state': 'DC', 'zipcode': '20500'},
		follow_redirects=True
	)
	# follow_redirects: Make additional requests to follow HTTP redirects until a non-redirect status is returned.
	# Check that there was one redirect response.
	assert len(response.history) == 1
	# Check that the redirect request was for the profile page.
	assert response.request.path == "/profile"

def test_delete_profile(test_client,conn,hash):
	username ="Delete_him"
	password = "secret_secret"
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
	# response = test_client.post('/profile/delete', data={'password': password}, follow_redirects=True)
	# assert response.status_code == 200
	# assert response.request.path == "/"
	with test_client.session_transaction() as s:
		s['username'] =username
	response = test_client.post(
			'/profile/delete',
			method = 'POST', 
			data={'password': password},  # Invalid password
			follow_redirects=True
		)

		# Assert that the response status code is 200 (OK)
	assert response.status_code == 200

	# 	# Test with valid form data. Populating the form fields by passing in a dictionary to 'data'.
	# response = test_client.post(
	# 		'/profile/delete',
	# 		data={'password': password},
	# 		follow_redirects=True
	# 	)
	# 	# Check that there was one redirect response.
	# assert len(response.history) == 1
	# 	# Check that the redirect request was for the profile page.
	# assert response.request.path == "/signup"
	# 	# test with invalid form data
	# response = test_client.post(
	# 		'/profile/delete',
	# 		data={'password': ''},
	# 		follow_redirects=True
	# 	)
	# assert response.status_code == 200