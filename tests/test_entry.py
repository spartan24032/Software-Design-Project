import pytest
import hashlib


def test_login_get(test_client):
    
    response = test_client.get('/login')
    # Test if get request is successful
    assert response.status_code == 200


def test_signup_get(test_client):
    response = test_client.get('/signup')
    # Test if get request is successful
    assert response.status_code == 200
# Import necessary libraries and modules



# Define a test function that uses the test_client and conn fixtures
def test_login(test_client, conn,hash):
    # Perform test actions using the conn fixture
    # For example, execute SQL queries to insert test data into the database
    # with conn.cursor() as cursor:
    #     query = "DELETE FROM UserCredentials where username =%s"
    #     cursor.execute(query,"username")
    # conn.commit()

    # with conn.cursor() as cursor:
    #     query = "INSERT INTO UserCredentials (username, encrypted_password) VALUES (%s,%s)"
    #     vals= ("username",hash("password"))
    #     cursor.execute(query,vals)
    # conn.commit()

    response = test_client.post('/login', data={'username': 'test_user23', 'encrypted_password': hash("password")})
    

    assert response.status_code == 200

# def test_sign_up(test_client, conn,hash):
#     # Perform test actions using the conn fixture
#     # For example, execute SQL queries to insert test data into the database
#     with conn.cursor() as cursor:
#         query = "DELETE FROM UserCredentials where username =%s"
#         cursor.execute(query,"username")
#     conn.commit()

#     info = test_client.post ('/signup', data = )

#     with conn.cursor() as cursor:
#         query = "INSERT INTO UserCredentials (username, encrypted_password) VALUES (%s,%s)"
#         vals= ("username",hash("password"))
#         cursor.execute(query,vals)
#     conn.commit()

    
    

#     assert response.status_code == 200
