import pytest
from unittest.mock import patch
from flask import Flask
from a2d.routes.reset import reset_routes

@pytest.fixture
def app():
    """Fixture to create a Flask app instance."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(reset_routes)
    app.secret_key = 'test_secret_key'  # Set a secret key for session management
    return app

@pytest.fixture
def client(app):
    """Fixture to create a test client with app context."""
    with app.test_client() as client:
        with app.app_context():
            yield client

def test_reset_account(client):
    """Test case for resetting account with valid passphrase."""
    with client.session_transaction() as sess:
        sess['user_id'] = 1  # Example user ID

    # Mock passphrase verification and form data
    with patch('a2d.routes.reset.verify_passphrase', return_value=True):
        data = {
            'passphrase': 'testpassphrase',
            'reset_confirm': 'delete',
            'self_ssl_delete': 'true',
            'ca_ssl_delete': 'false'
        }
        rv = client.post('/reset-portal', data=data)
        
        assert rv.status_code == 302  # Expecting redirect upon successful reset

def test_reset_account_invalid_passphrase(client):
    """Test case for resetting account with invalid passphrase."""
    with client.session_transaction() as sess:
        sess['user_id'] = 1  # Example user ID

    # Mock invalid passphrase verification
    with patch('a2d.routes.reset.verify_passphrase', return_value=False):
        data = {
            'passphrase': 'wrongpass',
            'reset_confirm': 'delete',
            'self_ssl_delete': 'true',
            'ca_ssl_delete': 'false'
        }
        rv = client.post('/reset-portal', data=data)
        
        assert rv.status_code == 302  # Expecting redirect upon failure due to invalid passphrase

def test_reset_account_no_confirmation(client):
    """Test case for resetting account without confirmation."""
    with client.session_transaction() as sess:
        sess['user_id'] = 1  # Example user ID

    # No confirmation provided
    data = {
        'passphrase': 'testpassphrase',
        'reset_confirm': '',
        'self_ssl_delete': 'false',
        'ca_ssl_delete': 'false'
    }
    rv = client.post('/reset-portal', data=data)
    
    assert rv.status_code == 302  # Expecting redirect or another appropriate status code

def test_reset_account_no_login(client):
    """Test case for resetting account without user logged in."""
    # No user logged in scenario
    data = {
        'passphrase': 'testpassphrase',
        'reset_confirm': 'delete',
        'self_ssl_delete': 'true',
        'ca_ssl_delete': 'false'
    }
    rv = client.post('/reset-portal', data=data, follow_redirects=True)
    
    assert rv.status_code == 404  # Expecting 404 when endpoint is not reachable without login
