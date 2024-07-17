import pytest
import importlib.resources

# Load gunicorn configuration
def load_gunicorn_config():
    gunicorn_config = {}
    a2d_files = importlib.resources.files('a2d')
    config_path = a2d_files / 'gunicorn_config.py'
    
    with config_path.open() as f:
        exec(f.read(), gunicorn_config)
    
    return gunicorn_config

# Test for checking if gunicorn.conf.py exists
def test_config_file_exists():
    a2d_files = importlib.resources.files('a2d')
    config_path = a2d_files / 'gunicorn_config.py'
    assert config_path.exists(), "gunicorn.conf.py file does not exist"

# Parameterized test for each configuration key
@pytest.mark.parametrize('key', [
    'bind',
    'workers',
    'threads',
    'max_requests',
    'max_requests_jitter',
    'timeout',
    'errorlog',
    'loglevel',
    'logrotate'
])
def test_gunicorn_config_keys(key):
    gunicorn_config = load_gunicorn_config()
    assert key in gunicorn_config, f"Key '{key}' not found in gunicorn config"
