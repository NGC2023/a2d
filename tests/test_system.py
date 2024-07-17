import pytest
from unittest.mock import patch
from flask import Flask
from a2d.routes.system import system_routes

@pytest.fixture
def client():
    app = create_app()
    app.register_blueprint(system_routes)

    with app.test_client() as client:
        with app.app_context():
            yield client

def create_app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.secret_key = 'your_secret_key'  # Example secret key for session
    return app

def test_system_info(client):
    with client.session_transaction() as sess:
        sess['user_id'] = 1  # Example user ID

    # Mocking get_cpu_temperature, get_system_memory_usage, and get_cpu_load
    with patch('a2d.routes.system.get_cpu_temperature', return_value=50.0), \
         patch('a2d.routes.system.get_system_memory_usage', return_value=50.0), \
         patch('a2d.routes.system.get_cpu_load', return_value=50.0):

        rv = client.get('/system-info')
        assert rv.status_code == 302  # Expecting a redirect

def test_system_info_no_login(client):
    # User not logged in
    rv = client.get('/system-info')
    assert rv.status_code == 302  # Redirect to login page or another location
