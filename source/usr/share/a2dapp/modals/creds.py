import os
import configparser
from cryptography.fernet import Fernet
import io

encryption_key = '/etc/a2d/.keys/a2d_AnDinfo.key'
a2d_config_file = '/etc/a2d/.creds/a2d_AnDinfo.conf'

def generate_encryption_key():
    if not os.path.exists(encryption_key):
        key = Fernet.generate_key()
        with open(encryption_key, 'wb') as key_file:
            key_file.write(key)
        # Change permissions to 400
        os.chmod(encryption_key, 0o400)
    return encryption_key

def encrypt_config(config):
    generate_encryption_key()  # Ensure encryption key file exists
    with open(encryption_key, 'rb') as keyfile:
        key = keyfile.read()
    cipher = Fernet(key)
    config_buffer = io.StringIO()
    config.write(config_buffer)
    serialized_config = config_buffer.getvalue().encode()
    encrypted_config = cipher.encrypt(serialized_config)
    return encrypted_config

def decrypt_config(config_path):
    with open(config_path, 'rb') as configfile:
        encrypted_config = configfile.read()
    with open(encryption_key, 'rb') as keyfile:
        key = keyfile.read()
    cipher = Fernet(key)
    decrypted_config = cipher.decrypt(encrypted_config)
    config = configparser.ConfigParser()
    config.read_string(decrypted_config.decode())
    return config

def save_credentials(callsign, txgroup, dapnetuser, dapnetpass, aprsapi):
    config = configparser.ConfigParser()
    config['DEFAULT'] = {
        'callsign_nossid': callsign,
        'txgroup': txgroup,
        'DAPNET_USER': dapnetuser,
        'DAPNET_PASS': dapnetpass,
        'APRSAPI_KEY': aprsapi
    }
    encrypted_config = encrypt_config(config)
    with open(a2d_config_file, 'wb') as configfile:
        configfile.write(encrypted_config)

def get_credentials():
    config_path = a2d_config_file
    if os.path.isfile(config_path):
        config = decrypt_config(config_path)
        callsign = config.get('DEFAULT', 'callsign_nossid', fallback='')
        txgroup = config.get('DEFAULT', 'txgroup', fallback='')
        dapnetuser = config.get('DEFAULT', 'DAPNET_USER', fallback='')
        dapnetpass = config.get('DEFAULT', 'DAPNET_PASS', fallback='')
        return {
            'callsign': callsign,
            'txgroup': txgroup,
            'dapnetuser': dapnetuser,
            'dapnetpass': dapnetpass,
        }
    else:
        return {'message': 'Input credentials.'}
