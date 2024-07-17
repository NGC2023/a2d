import pytest
from unittest.mock import patch
from flask import Flask
from a2d.routes.data import data_routes

@pytest.fixture
def client():
    app = create_app()
    app.register_blueprint(data_routes)

    with app.test_client() as client:
        with app.app_context():
            yield client

def create_app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.secret_key = 'your_secret_key'  # Example secret key for session
    return app

def test_fetch_logs(client):
    with client.session_transaction() as sess:
        sess['user_id'] = 1  # Example user ID

    # Mocking the database query and configparser read
    with patch('os.path.exists', side_effect=lambda x: True), \
         patch('sqlite3.connect') as mock_connect, \
         patch('configparser.ConfigParser') as MockConfigParser:

        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_cursor.fetchall.side_effect = [
            [(1, 'msg1', 'content1', '2023-01-01 10:00:00')],
            [(2, 'msg2', 'content2', '2023-01-01 11:00:00')]
        ]

        # Simulate a GET request
        rv = client.get('/fetch-logs')
        assert rv.status_code == 302

def test_fetch_logs_no_login(client):
    # User not logged in
    rv = client.get('/fetch-logs')
    assert rv.status_code == 302  # Expect redirect to login page or another location
