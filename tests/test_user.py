from flask import session
from app import users, User, get_userID, get_clientID

def test_create_user(test_client):
	username = "test_user"
	password = "test_pass"

	user = User(username, password)
	assert user.get_username() != "" and user.get_password() != ""

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