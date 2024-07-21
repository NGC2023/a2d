import os
import tempfile
import pytest
from a2d.app import app

@pytest.fixture
def client():
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            pass
        yield client
    os.close(db_fd)
    os.unlink(app.config['DATABASE'])

def test_home_route(client):
    """Test the home route."""
    rv = client.get('/')
    assert rv.status_code == 302  # Should redirect to /login if no session

def test_get_version(client):
    """Test the version route."""
    rv = client.get('/version')
    assert rv.status_code == 200
    assert rv.json == {'version': '2.0.5'}

def test_session_key_generation(monkeypatch):
    """Test session key generation and loading."""
    import tempfile
    import a2d.app
    
    with tempfile.TemporaryDirectory() as tempdir:
        SESSION_KEY_FILE = os.path.join(tempdir, "session_key.bin")
        
        def mock_generate_and_store_session_key():
            session_key = os.urandom(32)
            with open(SESSION_KEY_FILE, "wb") as key_file:
                key_file.write(session_key)
        
        def mock_load_session_key():
            try:
                with open(SESSION_KEY_FILE, "rb") as key_file:
                    return key_file.read()
            except FileNotFoundError:
                return None
        
        monkeypatch.setattr(a2d.app, "generate_and_store_session_key", mock_generate_and_store_session_key)
        monkeypatch.setattr(a2d.app, "load_session_key", mock_load_session_key)
        
        a2d.app.generate_and_store_session_key()
        session_key = a2d.app.load_session_key()
        
        assert session_key is not None
        assert len(session_key) == 32

def test_blueprints_registered():
    """Test if all blueprints are registered."""
    expected_blueprints = [
        'auth',
        'run',
        'dns',
        'system',
        'network',
        'config',
        'reset',
        'data'
    ]
    registered_blueprints = list(app.blueprints.keys())
    
    for blueprint in expected_blueprints:
        assert blueprint in registered_blueprints
