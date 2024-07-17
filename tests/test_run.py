import pytest
from unittest.mock import patch, MagicMock
from a2d.app import app
from a2d.routes.run import add_cronjob

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

def test_add_and_check_cronjob(monkeypatch):
    # Mocking filesystem operations for add_cronjob and check_cronjob functions
    mock_file = MagicMock()
    mock_open = MagicMock(return_value=mock_file)
    monkeypatch.setattr('builtins.open', mock_open)

    # Mocking ConfigParser to return a mock instance
    with patch('a2d.routes.run.configparser.ConfigParser') as MockConfigParser:
        mock_config = MockConfigParser.return_value
        mock_config.read.return_value = []  # Simulate an empty configuration file

        # Test adding cron job
        add_cronjob()

        # Assert that the file was opened correctly
        mock_open.assert_called_once_with('/etc/cron.d/a2d', 'a')

def test_service_routes(client):
    # Test start-service route
    rv = client.get('/start-service')
    assert rv.status_code == 302  # Redirects to '/' on success

    # Test stop-service route
    rv = client.get('/stop-service')
    assert rv.status_code == 302  # Redirects to '/' on success
