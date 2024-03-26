import pytest
from flask_app.forms.profile_form import EditProfile, DeleteProfile
    
def test_profile_get(test_client):
	response = test_client.get('/profile')
	# Test if get request is successful
	assert response.status_code == 200

def test_edit_profile(test_client):
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

def test_delete_profile(test_client):
	# Test with valid form data. Populating the form fields by passing in a dictionary to 'data'.
	response = test_client.post(
		'/profile/delete',
		data={'password': 'mock'},
		follow_redirects=True
	)
	# Check that there was one redirect response.
	assert len(response.history) == 1
	# Check that the redirect request was for the profile page.
	assert response.request.path == "/login"