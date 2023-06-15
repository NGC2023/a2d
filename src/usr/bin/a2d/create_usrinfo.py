import os
import configparser
import cryptography
from cryptography.fernet import Fernet

# Specify the directory and file paths
directory_path = "/etc/a2d"
encrypted_file_path = os.path.join(directory_path, "user_info_encr.conf")
key_file_path = "/usr/bin/a2d/a2d_usrk.bin"
initial_config = """[DEFAULT]
callsign_nossid = YOUR_CALLSIGN_WITHOUT_SSID_ALL_CAPS
txgroup = YOUR_DAPNET_TRANSMITTER_GROUP
DAPNET_USER = YOUR_DAPNET_USERNAME
DAPNET_PASS = YOUR_DAPNET_PASSWORD
APRSAPI_KEY = YOUR_APRS_API_KEY"""

# Generate or load the encryption key
if os.path.exists(key_file_path):
    with open(key_file_path, "rb") as key_file:
        encryption_key = key_file.read()
else:
    encryption_key = Fernet.generate_key()
    with open(key_file_path, "wb") as key_file:
        key_file.write(encryption_key)

# Create the directory if it doesn't exist
if not os.path.exists(directory_path):
    os.makedirs(directory_path)

# Create the encrypted configuration file with initial content if it doesn't exist
if not os.path.exists(encrypted_file_path):
    cipher = Fernet(encryption_key)
    encrypted_content = cipher.encrypt(initial_config.encode())
    with open(encrypted_file_path, "wb") as encrypted_file:
        encrypted_file.write(encrypted_content)

# Load the encrypted configuration file
with open(encrypted_file_path, "rb") as encrypted_file:
    encrypted_content = encrypted_file.read()

# Decrypt the configuration using the encryption key
try:
    cipher = Fernet(encryption_key)
    decrypted_content = cipher.decrypt(encrypted_content)
except cryptography.fernet.InvalidToken:
    print("Invalid encryption key. Regenerating key and decrypting the default configuration.")
    encryption_key = Fernet.generate_key()
    cipher = Fernet(encryption_key)
    decrypted_content = cipher.decrypt(encrypted_content)

# Convert the decrypted content to a string
decrypted_content_str = decrypted_content.decode().strip()

# Check if the decrypted content matches the initial default configuration
is_default_config = (decrypted_content_str == initial_config.strip())

# Prompt the user to modify the configuration if it is still the default
if is_default_config:
    print("The configuration is still the default. Please modify the configuration.")
    input("Press Enter to continue...")

# Save the decrypted content to a temporary file for editing
temp_file_path = "/tmp/user_info.conf"
with open(temp_file_path, "wb") as temp_file:
    temp_file.write(decrypted_content)

# Open the temporary file in an editor for the user to make changes
editor_command = f"nano {temp_file_path}"
os.system(editor_command)

# Read the edited content from the temporary file
with open(temp_file_path, "rb") as temp_file:
    edited_content = temp_file.read()

# Encrypt the edited content using the encryption key
encrypted_content = cipher.encrypt(edited_content)

# Save the encrypted content back to the file
with open(encrypted_file_path, "wb") as encrypted_file:
    encrypted_file.write(encrypted_content)

# Remove the temporary file
os.remove(temp_file_path)
