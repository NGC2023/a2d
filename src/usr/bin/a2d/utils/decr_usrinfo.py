import os
from cryptography.fernet import Fernet

def retrieve_usrinfo():
    key_file = '/usr/bin/a2d/a2d_usrk.bin'
    encrypted_file = '/etc/a2d/user_info_encr.conf'

    with open(key_file, 'rb') as file:
        key = file.read()

    cipher_suite = Fernet(key)

    with open(encrypted_file, 'rb') as file:
        encrypted_data = file.read()

    decrypted_data = cipher_suite.decrypt(encrypted_data).decode('utf-8')

    # Parse the decrypted data as needed
    data_dict = {}
    for line in decrypted_data.split('\n'):
        line = line.strip()
        if line and ' = ' in line:
            key, value = line.split(' = ', 1)
            data_dict[key] = value

    return data_dict
