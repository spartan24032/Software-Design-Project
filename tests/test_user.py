from flask import session
from app import users, User

def test_create_user(test_client):
	username = "test_user"
	password = "test_pass"

	user = User(username, password)
	assert user.get_username() != ""

def test_edit_user(test_client):
	username = "test_user"
	password = "test_pass"

	# sign up and log in to set session cookie
	response_signup = test_client.post(
		'/signup',
		data={'username': username, 'password': password},
		follow_redirects=True
	)
	assert response_signup.status_code == 200

	response_login = test_client.post(
		'/login',
		data={'username': username, 'password': password, 'confirm_password': password},
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
	session["username"] = ""
	response_edit = test_client.post(
		'/profile/edit',
		data={'name': name, 'address1': address1, 'address2': address2, 'city': city, 'state': state, 'zipcode': zipcode},
		follow_redirects=True
	)
	assert len(response_edit.history) == 1
	assert response_edit.request.path == "/profile"

def test_delete_user(test_client):
	username = "test_user"
	password = "test_pass"

	# sign up and log in to set session cookie
	response_signup = test_client.post(
		'/signup',
		data={'username': username, 'password': password},
		follow_redirects=True
	)
	assert response_signup.status_code == 200

	response_login = test_client.post(
		'/login',
		data={'username': username, 'password': password, 'confirm_password': password},
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
	assert response_delete.request.path == "/signup"

	# test unsuccessful deletion
	session["username"] = ""
	user = User(username, password)
	users.append(user)
	response_delete = test_client.post(
		'/profile/delete',
		data={'password': password},
		follow_redirects=True
	)
	assert len(response_delete.history) == 1
	assert response_delete.request.path == "/signup"
