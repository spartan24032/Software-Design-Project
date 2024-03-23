import pytest
from flask_app.forms.profile_form import ProfileForm
    
def test_profile_get(test_client):
	response = test_client.get('/profile')
	# test if get request is successful
	assert response.status_code == 200

# TODO: Add Not Applicable option for address 2 in form
def test_profile_post(test_client):
	# test with valid form data. populating form fields and assigning to the 'data' argument
	response = test_client.post(
		'/profile',
		data={'name': 'President', 'address1': '1600 Pennsylvania Avenue, N.W.', 'address2': 'Not Applicable', 'city': 'Washington', 'state': 'DC', 'zipcode': '20500'},
		follow_redirects=True
	)
	# follow_redirects: Make additional requests to follow HTTP redirects until a non-redirect status is returned.
	# Check that there was one redirect response.
	assert len(response.history) == 1
	# Check that the second request was to the index page.
	assert response.request.path == "/profile"