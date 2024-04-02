import pytest

def test_login_get(test_client):
    response = test_client.get('/login')
    # Test if get request is successful
    assert response.status_code == 200

def test_login_post(test_client):
    username = "test_user"
    password = "test_pass"

	# sign up and log in to set session cookie
    response_signup = test_client.post(
		'/signup',
		data={'username': username, 'password': password},
		follow_redirects=True
	)
    assert response_signup.status_code == 200

    fake_username = "fake"
    response_login = test_client.post(
		'/login',
		data={'username': fake_username, 'password': password, 'confirm_password': password},
		follow_redirects=True
	)
    assert response_login.data == b'<h1>invalid credentials!</h1>'


def test_signup_get(test_client):
    response = test_client.get('/signup')
    # Test if get request is successful
    assert response.status_code == 200
