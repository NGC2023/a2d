from cryptography.fernet import Fernet
import os

encryption_key_file = '/etc/a2d/.keys/app.key'
passphrase_key_file = '/etc/a2d/.keys/passphrase.key'
user_pin_file = '/etc/a2d/.creds/user_pin.bin'
user_passphrase_file = '/etc/a2d/.creds/user_passphrase.bin'
cipher = None

def generate_encryption_key():
    encryption_key = Fernet.generate_key()
    os.makedirs(os.path.dirname(encryption_key_file), exist_ok=True)
    with open(encryption_key_file, 'wb') as key_file:
        key_file.write(encryption_key)
    # Change permissions to 400
    if os.path.exists(encryption_key_file):
        os.chmod(encryption_key_file, 0o400)
    return encryption_key

def get_encryption_key():
    if os.path.isfile(encryption_key_file):
        with open(encryption_key_file, 'rb') as key_file:
            encryption_key = key_file.read()
    else:
        encryption_key = generate_encryption_key()
    return encryption_key

def verify_pin(pin):
    encryption_key = get_encryption_key()
    cipher = Fernet(encryption_key)
    with open(user_pin_file, 'rb') as file:
        encrypted_pin = file.read()
        decrypted_pin = cipher.decrypt(encrypted_pin).decode()
        if pin == decrypted_pin:
            return True
    return False

def create_user(pin):
    encryption_key = get_encryption_key()
    os.makedirs(os.path.dirname(user_pin_file), exist_ok=True)
    cipher = Fernet(encryption_key)
    encrypted_pin = cipher.encrypt(pin.encode())
    with open(user_pin_file, 'wb') as file:
        file.write(encrypted_pin)

def generate_passphrase_key():
    encryption_key = Fernet.generate_key()
    os.makedirs(os.path.dirname(passphrase_key_file), exist_ok=True)
    with open(passphrase_key_file, 'wb') as key_file:
        key_file.write(encryption_key)
    # Change permissions to 400
    if os.path.exists(passphrase_key_file):
        os.chmod(passphrase_key_file, 0o400)
    return encryption_key

def get_passphrase_key():
    if os.path.isfile(passphrase_key_file):
        with open(passphrase_key_file, 'rb') as key_file:
            encryption_key = key_file.read()
    else:
        encryption_key = generate_passphrase_key()
    return encryption_key

def decrypt_user_passphrase():
    encryption_key = get_passphrase_key()
    cipher = Fernet(encryption_key)
    with open(user_passphrase_file, 'rb') as file:
        encrypted_passphrase = file.read()
        decrypted_passphrase = cipher.decrypt(encrypted_passphrase).decode()
    return decrypted_passphrase

def create_user_passphrase(passphrase):
    encryption_key = get_passphrase_key()
    cipher = Fernet(encryption_key)
    encrypted_passphrase = cipher.encrypt(passphrase.encode())
    with open(user_passphrase_file, 'wb') as file:
        file.write(encrypted_passphrase)