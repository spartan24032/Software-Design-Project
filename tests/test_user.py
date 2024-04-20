from flask import session
from app import users, User, get_userID, get_clientID

def test_create_user(test_client):
	username = "test_user"
	password = "test_pass"

	user = User(username, password)
	assert user.get_username() != "" and user.get_password() != ""

def test_edit_user(test_client):
	username = "test_user"
	password = "test_pass"

	response_signup = test_client.post(
		'/signup',
		data={'username': username, 'password': password, 'confirm_password': password},
		follow_redirects=True
	)
	assert response_signup.status_code == 200

	response_login = test_client.post(
		'/login',
		data={'username': username, 'password': password},
		follow_redirects=True
	)
	assert response_login.status_code == 200

	name = "President"
	address1 = "1600 Pennsylvania Avenue, N.W."
	address2 = ""
	city = "Washington, D.C."
	state = "DC"
	zipcode = "20500"

	# test successful edit
	response_edit = test_client.post(
		'/profile/edit',
		data={'name': name, 'address1': address1, 'address2': address2, 'city': city, 'state': state, 'zipcode': zipcode},
		follow_redirects=True
	)
	# Check that there was one redirect response.
	assert len(response_edit.history) == 1
	# Check that the redirect request was for the profile page.
	assert response_edit.request.path == "/profile"

	# test unsuccessful edit
	with test_client.session_transaction() as session:
		session["username"] = "test_user"

	response_edit = test_client.post(
		'/profile/edit',
		data={'name': name, 'address1': address1, 'address2': address2, 'city': city, 'state': state, 'zipcode': zipcode},
		follow_redirects=True
	)
	assert len(response_edit.history) == 1
	assert response_edit.request.path == "/profile"

def test_delete_user(test_client):
	username = "test_user2"
	password = "test_pass2"

	# sign up and log in to set session cookie
	response_signup = test_client.post(
		'/signup',
		data={'username': username, 'password': password, 'confirm_password': password},
		follow_redirects=True
	)
	assert response_signup.status_code == 200

	response_login = test_client.post(
		'/login',
		data={'username': username, 'password': password},
		follow_redirects=True
	)
	assert response_login.status_code == 200

	# test successful deletion
	response_delete = test_client.post(
		'/profile/delete',
		data={'password': password},
		follow_redirects=True
	)
	assert len(response_delete.history) == 1
	assert response_delete.request.path == "/"

	# test unsuccessful deletion
	with test_client.session_transaction() as session:
		session["username"] = ""

	user = User(username, password)
	users.append(user)
	response_delete = test_client.post(
		'/profile/delete',
		data={'password': password},
		follow_redirects=True
	)
	# after deletion, redirect to homepage
	assert len(response_delete.history) == 1
	assert response_delete.request.path == "/"

def test_get_user_ID( test_client, conn, hash):
	
	username = 'test_user23'
	password = 'test_pass23'

	# Delete duplicate username, if any
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
	ph = dict()
	ph['username'] = username
	assert (get_userID(ph))