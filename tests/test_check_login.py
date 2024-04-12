from app import check_login
import pytest

known_username = 'test_user_login'
known_password = 'test_pass_login'
unknown_username = 'test_user_not_exist'
unknown_password = 'test_pass_login_not_exist'

@pytest.fixture
def setup_test_data(conn, hash):
    # Delete any existing test data
    with conn.cursor() as cursor:
        query = "DELETE FROM UserCredentials WHERE username IN (%s, %s)"
        cursor.execute(query, (known_username, unknown_username))
    conn.commit()

    # Insert known login credentials
    with conn.cursor() as cursor:
        query = "INSERT INTO UserCredentials (username, encrypted_password) VALUES (%s, %s)"
        vals = [(known_username, hash(known_password))]
        cursor.executemany(query, vals)
    conn.commit()

    yield

@pytest.mark.parametrize("username, password, expected_result", [
    (known_username, known_password, True),  # Correct username and correct password
    (known_username, unknown_password, False),  # Correct username and incorrect password
    (unknown_username, known_password, False),  # Incorrect username and correct password
    (unknown_username, unknown_password, False),  # Incorrect username and incorrect password
    (known_username, '', False),  # Correct username and empty password
    ('', known_password, False),  # Empty username and correct password
    ('', '', False),  # Empty username and empty password
    ('non_existent_user', known_password, False),  # Non-existent username
    ('non_existent_user', '', False),  # Non-existent username and empty password
    ('', 'non_existent_password', False),  # Empty username and non-existent password
])
def test_check_login(setup_test_data, username, password, expected_result):
    assert check_login(username, password) == expected_result
