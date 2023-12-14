# Test homepage
def test_homepage(test_app):
    response = test_app.get('/')
    assert response.status_code == 200

# Test create event
def test_create_event(test_app):
    response = test_app.get('/create')
    assert response.status_code == 200

# Test event search 
def test_event_search(test_app):
    response = test_app.get('/events/search')
    assert response.status_code == 200

# Test friends page
def test_friends_page(test_app):
    response = test_app.get('/friends')
    assert response.status_code == 200

# About Page
def test_about_page(test_app):
    response = test_app.get('/about')
    assert response.status_code == 200

# FAQ
def test_faq_page(test_app):
    response = test_app.get('/FAQ')
    assert response.status_code == 200

def test_account_faq_page(test_app):
    response = test_app.get('/FAQ/account')
    assert response.status_code == 200

def test_events_faq_page(test_app):
    response = test_app.get('/FAQ/events')
    assert response.status_code == 200

# Login
def test_login_page(test_app):
    response = test_app.get('/login')
    assert response.status_code == 200

# Profile
def test_profile_page(test_app):
    response = test_app.get('/profile')
    assert response.status_code == 200

# Settings
def test_settings_page(test_app):
    response = test_app.get('/settings')
    assert response.status_code == 200

# Sign up
def test_signup_page(test_app):
    response = test_app.get('/sign_up')
    assert response.status_code == 200